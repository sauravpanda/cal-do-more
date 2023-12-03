import boto3
import json
import os
import requests

flask_url = os.environ["FLASK_URL"]

region_name='us-east-2'
aws_access_key_id=os.environ['AWS_ACCESS_KEY']
aws_secret_access_key=os.environ['AWS_SECRET_KEY']


def setup_s3_trigger():
    s3 = boto3.client(service_name='s3',
                  region_name=region_name,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    lambda_client = boto3.client(service_name='lambda',
                                region_name=region_name,
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)

    iam = boto3.client(service_name='iam',
                    region_name=region_name,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

    lambda_role_arn = lambda_client.get_function_configuration(FunctionName='cal_video_transcription')['Role']
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

    lambda_function_arn = lambda_client.get_function(FunctionName='cal_video_transcription')['Configuration']['FunctionArn']

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
    return "trigger set up for lambda"
