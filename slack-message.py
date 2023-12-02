import os
import requests


# Replace this URL with your Slack incoming webhook URL
slack_webhook_url = os.getenv("SLACK_HOOK")

# Set up the request payload with interactive message components
payload = {
    "text": "Do you agree with the statement? You'll see an image if you click on the buttons",
    "attachments": [
        {
            "text": "Choose an option:",
            "fallback": "You are unable to choose an option",
            "callback_id": "yes_no_callback",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "answer",
                    "text": "Yes",
                    "type": "button",
                    "value": "Create a new event",
                    "url": "https://app.cal.com/event-types?dialog=new&eventPage=parthit-music-klhypg"  # Replace with your actual URL
                },
                {
                    "name": "answer",
                    "text": "No",
                    "type": "button",
                    "value": "no",
                    "url": "http://127.0.0.1:5000/response"  # Replace with your actual URL
                }
            ]
        }
    ]
}

# Make the POST request to the Slack incoming webhook URL
response = requests.post(slack_webhook_url, json=payload)

# Check the response status
if response.status_code == 200:
    print("Question sent successfully.")
else:
    print(f"Error sending question to Slack: {response.status_code}, {response.text}")

