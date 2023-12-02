import os
from dotenv import load_dotenv
import time
import json 
import datetime
import boto3
from openai import OpenAI

load_dotenv()

# Access the variables
org_var = os.getenv("ORG_VAR")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set your AWS credentials (replace 'your_access_key' and 'your_secret_key' with your actual credentials)
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Specify the S3 bucket name and key (object/key name)
bucket_name = 'osshackathon-audio'
object_key = 'two-people-audio.m4a'

# Example: List all objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)
for obj in response.get('Contents', []):
    print(f"Object Key: {obj['Key']}, Last Modified: {obj['LastModified']}")

local_path = './audio-folder/two-people-audio.m4a'
s3.download_file(bucket_name, object_key, local_path)

print(f"File downloaded to: {local_path}")

client = OpenAI(api_key=openai_api_key)

audio_file= open("./audio-folder/two-people-audio.m4a", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

print(transcript.text)

import os

# Ensure the 'output' folder exists
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the output file path
output_file_path = os.path.join(output_folder, object_key+'_whisper.txt')

# Write the transcript text to the text file
with open(output_file_path, 'w') as output_file:
    output_file.write(transcript.text)

print(f"Transcription output saved to: {output_file_path}")