import boto3
import json
import os
import requests

flask_url = os.environ["FLASK_URL"]

def lambda_handler(event, context):
    api_url = flask_url + "/cal/video/transcribe"
    response = requests.post(api_url, json=event)
    return {
        "statusCode": response.status_code,
        "body": json.dumps(response)
    }
