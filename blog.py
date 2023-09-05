import requests
import json
import random
import logging
import time
from constants import *

# ==============================================================================
# Project: Automated Blog Posting with Personal.AI and LinkedIn Integration
# File: [Blog.py].py
# Author: Matthew David Schafer
# Date: Sept 5, 2023
# Company: VE7LTX Diagonal Thinking LTD
# ==============================================================================
# 
# Copyright (c) 2023, Matthew David Schafer, VE7LTX Diagonal Thinking LTD
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions, and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions, and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the company VE7LTX Diagonal Thinking LTD nor the names 
#    of its contributors may be used to endorse or promote products derived 
#    from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.


# Set up logging
logging.basicConfig(filename="blog.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s]: %(message)s")
logging.info("Script started.")

def ideas_left(filename='post_ideas.jsonl') -> bool:
    """Check if there are any ideas left in the file."""
    with open(filename, 'r') as file:
        ideas = [json.loads(line) for line in file]
    return bool(ideas)

class LinkedInAPIError(Exception):
    """Custom exception for LinkedIn API errors."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def send_message_to_linkedin(text: str) -> dict:
    """
    Send a message to LinkedIn.

    Parameters:
    - text (str): The text to send to LinkedIn.

    Returns:
    - dict: The response from LinkedIn.
    """
    logging.debug("Preparing to send message to LinkedIn")
    logging.debug(f"Text: {text}")

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "author": LINKEDIN_MEMBER_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    # Check for both 200 and 201 status codes as successful responses
    if response.status_code not in [200, 201]:
        logging.error(f"Error sending message to LinkedIn: {response.text}")
        raise LinkedInAPIError(f"LinkedIn API returned {response.status_code}: {response.text}", status_code=response.status_code)
    
    return response.json()

def get_linkedin_user_info() -> dict:
    """
    Fetch LinkedIn member details using the userinfo endpoint.

    Returns:
    - dict: Member details.
    """
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    member_info = response.json()
    logging.debug(f"LinkedIn member info: {member_info}")
    return member_info



def send_message_to_pai(text: str) -> dict:
    """
    Send a message to Personal.AI.

    Parameters:
    - text (str): The text to send to Personal.AI.

    Returns:
    - dict: The response from Personal.AI.
    """
    logging.debug("Preparing to send message to Personal.AI")
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': PAI_API_KEY
    }
    payload = {
        "Text": text
    }

    response = requests.post(f"{BASE_URL}/message", headers=headers, json=payload)
    response.raise_for_status()

    return response.json()


def pick_random_idea_from_file(filename='post_ideas.jsonl') -> dict:
    """Pick a random idea from a file."""
    with open(filename, 'r') as file:
        ideas = [json.loads(line) for line in file]

    if not ideas:
        logging.warning("No ideas found in the file")
        return None

    chosen_idea = random.choice(ideas)
    logging.debug(f"Chosen idea: {chosen_idea}")
    return chosen_idea


def remove_idea_from_file(idea: dict, filename='post_ideas.jsonl'):
    """Remove an idea from a file."""
    with open(filename, 'r') as file:
        ideas = [json.loads(line) for line in file]

    ideas = [i for i in ideas if i != idea]

    with open(filename, 'w') as file:
        for i in ideas:
            file.write(json.dumps(i) + '\n')
    logging.debug(f"Idea removed from file: {idea}")


def save_posted_idea(idea: dict, response: dict, filename='posted_posts.jsonl'):
    """Save a posted idea to a file."""
    post_info = {
        "original_idea": idea,
        "generated_post": response.get('ai_message'),
        "ai_score": response.get('ai_score')
    }

    with open(filename, 'a') as file:
        file.write(json.dumps(post_info) + '\n')
    logging.debug(f"Idea posted and saved: {idea}")



logging.info("Fetching LinkedIn Member URN...")
member_info = get_linkedin_user_info()
LINKEDIN_MEMBER_URN = f"urn:li:person:{member_info['sub']}"

logging.info(f"LinkedIn Member URN fetched: {LINKEDIN_MEMBER_URN}")

if __name__ == "__main__":
    logging.info("Script execution started.")
    print("Script execution started.")
    
    while ideas_left():  # Check if there are ideas left
        logging.info("Fetching random idea from file...")
        print("Fetching random idea from file...")
        idea = pick_random_idea_from_file()
        
        if idea:
            logging.info(f"Selected idea: {idea['text']}")
            print(f"Selected idea: {idea['text']}")
            
            # Send the idea to Personal.AI to generate the blog post
            logging.info("Sending idea to Personal.AI for blog post generation...")
            print("Sending idea to Personal.AI for blog post generation...")
            pai_response = send_message_to_pai(idea['text'])
            
            # Extract ai_message and ai_score from the Personal.AI response
            ai_message = pai_response.get('ai_message', "No valid message returned by Personal.AI")
            ai_score = pai_response.get('ai_score', "No AI score provided.")
            
            # Combine ai_message, ai_score, and DISCLAIMER for the final blog post
            generated_blog_post = f"{ai_message}\n\nAI Score: {ai_score}{DISCLAIMER}"
            logging.debug("Generated Blog Post:\n" + generated_blog_post)
            print("Generated Blog Post:\n" + generated_blog_post)
            
            # Send the generated blog post to LinkedIn
            logging.info("Sending generated blog post to LinkedIn...")
            print("Sending generated blog post to LinkedIn...")
            linkedin_response = send_message_to_linkedin(generated_blog_post)
            
            if linkedin_response:
                logging.info("Blog post successfully posted to LinkedIn!")
                print("Blog post successfully posted to LinkedIn!")
                logging.debug(f"LinkedIn response: {linkedin_response}")
                print(f"LinkedIn response: {linkedin_response}")
                save_posted_idea(idea, pai_response)
                remove_idea_from_file(idea)
            else:
                logging.error("No valid response received from the LinkedIn API")
                print("No valid response received from the LinkedIn API")
        else:
            logging.warning("No more post ideas left!")
            print("No more post ideas left!")
            break  # Exit the loop if no ideas left
        
        time.sleep(300)  # Sleep 5 min
    
    logging.info("No more ideas left in the list. Script execution completed gracefully.")
    print("No more ideas left in the list. Script execution completed gracefully.")
