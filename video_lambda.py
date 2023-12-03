import boto3
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

flask_url = os.environ["FLASK_URL"]

s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')
iam = boto3.client('iam')

lambda_role_arn = lambda_client.get_function_configuration(FunctionName='call_video_transcription')['Role']
iam.attach_role_policy(
    RoleName=lambda_role_arn.split('/')[-1],
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaS3ExecutionRole'
)
lambda_client.add_permission(
    FunctionName="cal_video_transcription",
    StatementId='s3-invoke-permission',
    Action='lambda:InvokeFunction',
    Principal='s3.amazonaws.com'
)

lambda_function_arn = lambda_client.get_function(FunctionName='call_video_transcription')['Configuration']['FunctionArn']

s3_event_configuration = {
    'LambdaFunctionConfigurations': [
        {
            'Id': '1',
            'LambdaFunctionArn': lambda_function_arn,
            'Events': ['s3:ObjectCreated:*']
        }
    ]
}

s3.put_bucket_notification_configuration(Bucket='osshackathon-audio', NotificationConfiguration=s3_event_configuration)


def call_video_transcription(payload):
    api_url = flask_url + "/cal/video/transcribe"
    response = requests.post(api_url, json=payload)
    return {
        "statusCode": response.status_code,
        "body": json.dumps(response)
    }
