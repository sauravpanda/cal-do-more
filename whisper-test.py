import os
from dotenv import load_dotenv

load_dotenv()

# Access the variables
org_var = os.getenv("ORG_VAR")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the variables in your code
print(f"Database URL: {org_var}")
print(f"API Key: {openai_api_key}")
