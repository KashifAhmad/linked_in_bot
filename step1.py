# ==============================================================================
# Project: Automated Blog Posting with Personal.AI and LinkedIn Integration
# File: [step1].py
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


"""
LinkedIn Company Page Fetcher

This script retrieves the user's company pages on LinkedIn where they have an 'ADMINISTRATOR' role.
Specifically, it makes use of the LinkedIn's Organizational Entity Access Control List API to fetch
the URNs (Uniform Resource Names) of company pages the authenticated user administers.

Instructions:
1. Replace `ACCESS_TOKEN` with the user's LinkedIn access token.
    - This token can typically be obtained after OAuth authentication with LinkedIn.
    - Ensure the token has the necessary permissions/scopes to read organizational data.
    
2. The `HEADERS` dictionary is set up to carry the access token for authentication with LinkedIn's API.

3. The script then makes a GET request to LinkedIn's API to fetch company pages where the user has 
   an 'ADMINISTRATOR' role.

4. The response is parsed to retrieve the URN of the company page. For simplicity, this example assumes 
   the user has only one company page. If a user administers multiple pages, consider iterating over the 
   `company_pages_data["elements"]` list.

Remember: Always keep access tokens confidential. Store securely and never expose them in client-side code 
or public repositories.
"""


import requests

ACCESS_TOKEN = "AQVEFlu_MjwuSPI7udFa3asAWhBXv2E6gbKASWf2w997nveU2W94mDxrmHaYgWkwiW968wSAF2fByhQRmuIutIQHbbEQf-aB_kEn1DywhdxbF_eYM_7bPBKIB8KQAv_iJCe_WKTsi4NGCnb_pfzXE0FMeEftVMguiMLMORp-iKau6NcsGB7cLwlhObW8EY5RfcIrShs3DAb-1zHLbj2iMcghqGSo79sq6Q-RVi3SE4mh9TH-hT1kPrNPEg9FBt49YgC5Kr76BEu1HNxH5EkXAtwuVn-wkPxhdalXF3ccxyyyhoWwPXho9S0i02uh3vXyCJeIwiZS-2LEK9MP1J4l-FJvFtn-hA"  # Replace with the user's access token
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Fetch user's company pages
company_pages_url = "https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee&role=ADMINISTRATOR"
response = requests.get(company_pages_url, headers=HEADERS)
company_pages_data = response.json()

# Assuming there's only one company page in this example
if "elements" in company_pages_data and len(company_pages_data["elements"]) > 0:
    company_page = company_pages_data["elements"][0]
    person_urn = company_page["roleAssignee"]["id"]
    print("Person URN:", person_urn)
else:
    print("No company pages found.")



"""
Using the Retrieved URNs in Templates:

Once you have the URN of the company page or any other LinkedIn entity, you can integrate it into various LinkedIn API operations, templates, or scripts.

1. Posting to a Company Page:
   - Use the URN to post updates or articles on behalf of the company page.
   - Example API Endpoint: https://api.linkedin.com/v2/ugcPosts
   - Payload might look like: 
     {
       "author": "urn:li:organization:{organizationId}",   # Use the URN here
       "lifecycleState": "PUBLISHED",
       ...
     }

2. Retrieving Company Page Details:
   - Fetch detailed information about the company page using its URN.
   - Example Endpoint: https://api.linkedin.com/v2/organizations/{organizationId}

3. Integrating with Templates:
   - If you have predefined templates for posts, articles, or reports, simply insert the URN where required.
   - Example: "Check out our latest updates on [LinkedIn](https://www.linkedin.com/company/{organizationId})!"

4. Sharing URNs:
   - Share URNs with team members or scripts that need to perform operations on behalf of the company page.
   - Always ensure the access token remains confidential.

Remember, when using URNs in API operations, ensure you have the necessary permissions and are aware of LinkedIn's API usage limits and guidelines.

For more details on LinkedIn's API and how to use URNs, refer to LinkedIn's official API documentation.
"""
