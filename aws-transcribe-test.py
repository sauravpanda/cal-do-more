import os
from dotenv import load_dotenv
import time
import json 
import datetime
import boto3

load_dotenv()

# Access the variables
org_var = os.getenv("ORG_VAR")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the variables in your code
print(f"Database URL: {org_var}")
print(f"API Key: {openai_api_key}")


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

# Specify the AWS Transcribe job name
transcribe_job_name = 'oss-hack-transcribe-job-' + object_key

# Specify the language code and output format
language_code = 'en-US'
output_format = 'json'

output_json_bucket = 'osshackathon-audio-transcriptions'

transcribe = boto3.client('transcribe', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name='us-east-2')

# Start the transcription job
transcribe.start_transcription_job(
    TranscriptionJobName=transcribe_job_name,
    LanguageCode=language_code,
    MediaFormat='mp4',  # Change this to the appropriate format if needed
    Media={
        'MediaFileUri': f's3://{bucket_name}/{object_key}'
    },
    OutputBucketName=output_json_bucket,  # You can specify a different bucket for transcribe output
    Settings={
        'ShowSpeakerLabels': True,
        'MaxSpeakerLabels': 2
    }
)

transcription_text = ""

# Poll for the transcription job status
while True:
    response = transcribe.get_transcription_job(TranscriptionJobName=transcribe_job_name)
    status = response['TranscriptionJob']['TranscriptionJobStatus']
    print(f"Transcription job status: {status}")
    if status in ['COMPLETED', 'FAILED']:
        break
    
    time.sleep(10)  # Wait for 30 seconds before checking again

if status == 'COMPLETED':
    # Get the transcription job results
    transcription_results_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    object_key = transcribe_job_name + '.json'


    # Download and print the transcription results
    transcription_results = s3.get_object(Bucket=output_json_bucket, Key=object_key)
    transcription_text = transcription_results['Body'].read().decode('utf-8')
    print("Transcription Results:\n", transcription_text, '\n')
else:
    print(f"Transcription job failed with status: {status}")

# Load the JSON data
transcription_data = json.loads(transcription_text)

# Extract speaker labels and items from the transcription data
speaker_labels = transcription_data['results']['speaker_labels']
items = transcription_data['results']['items']

# Create a dictionary to map speaker labels to speaker names
speaker_mapping = {label['speaker_label']: f'speaker_{i}' for i, label in enumerate(speaker_labels['segments'])}

# Initialize variables
result_list = []
current_speaker = None
current_speech = ''
current_start_time = None
current_end_time = None
first_time_spoken_start_time = None
counter = 0

# Process each item in the transcription
for item in items:
    if item['type'] == 'pronunciation':
        speaker_label = item['speaker_label']
        if counter == 0:
            first_time_spoken_start_time = float(item['start_time'])
            counter += 1

        if current_speaker is None or current_speaker != speaker_label:
            # New speaker detected
            if current_speaker is not None:
                # Save the previous speaker's speech
                if counter == 1:
                    duration = current_end_time - first_time_spoken_start_time
                    result_list.append({
                        'speaker': speaker_mapping[current_speaker],
                        'speech': current_speech.strip(),
                        'time_spoken': f"{duration:.3f}"
                    })
                    counter = 0
                    first_time_spoken_start_time = current_end_time

            # Initialize for the new speaker
            current_speaker = speaker_label
            current_speech = item['alternatives'][0]['content']
            current_start_time = float(item['start_time'])
            current_end_time = float(item['end_time'])

        else:
            # Continue with the current speaker
            current_speech += ' ' + item['alternatives'][0]['content']
            current_start_time = float(item['start_time'])
            current_end_time = float(item['end_time'])

# Add the last speaker's speech
if current_speaker is not None:
    result_list.append({
        'speaker': speaker_mapping[current_speaker],
        'speech': current_speech.strip(),
        'time_spoken': f"{current_end_time - first_time_spoken_start_time:.3f}"
    })

for result in result_list:
    print(result)
