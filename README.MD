# Automated Blog Posting Using Personal.AI and LinkedIn API

## This script automates the process of generating AI-powered blog posts using Personal.AI and then posting them to LinkedIn.

### Prerequisites

    Python 3.x
    Required Python libraries: requests, json, random, logging, time

### Setup

    1. API Keys & Tokens:
        Replace placeholders in the constants.py file with your actual values:
            ACCESS_TOKEN : Your LinkedIn access token.
            PAI_API_KEY : Your Personal.AI API key.

    2. Logging:
        The script logs various events and exceptions. They are written to blog.log. Always refer to this log file for detailed script execution traces and debugging.

### Execution

    Run the script using:

        python blog.py