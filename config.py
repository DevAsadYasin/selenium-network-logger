import random
from dotenv import load_dotenv
import os

load_dotenv()

URLS = {
    'login': 'https://login.microsoftonline.com/',
    'people': 'https://outlook.office.com/people/'
}

FIRST_NAMES = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Lisa']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']

def generate_random_name():
    """Generate random first and last name"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return first_name, last_name

# Load sensitive data from environment variables (stored in .env file)
OUTLOOK_EMAIL = os.getenv('OUTLOOK_EMAIL')
OUTLOOK_PASSWORD = os.getenv('OUTLOOK_PASSWORD')
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL')

# Validate environment variables are set
if not all([OUTLOOK_EMAIL, OUTLOOK_PASSWORD, CONTACT_EMAIL]):
    raise ValueError("Missing required environment variables. Please check your .env file")
