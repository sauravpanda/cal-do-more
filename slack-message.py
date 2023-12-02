import requests
import os 

# Replace this URL with your Slack incoming webhook URL
slack_webhook_url= os.environ["SLACK_HOOK"]

# Specify the message text
message_text = "This call was made from Python by Parthit"

# Set up the request payload
payload = {
    "text": message_text
}

# Make the POST request to the Slack incoming webhook URL
response = requests.post(slack_webhook_url, json=payload)

# Check the response status
if response.status_code == 200:
    print("Message sent successfully.")
else:
    print(f"Error sending message to Slack: {response.status_code}, {response.text}")
