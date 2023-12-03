# cal-do-more
A personal AI Meeting assistant to schedule meetings and tasks based on video conversation. Ensures you dont miss out the task due to long meetings.

### The Idea:

Once a video conferencing ends, Cal stores the video files in S3 bucket.
From here:
- S3 buckets triggers cal-do-more to process the video
- Cal-do-more transcribes the video and parses them into topics discussed in the call
- It also identifies what are action tasks like Scheduling meeting and Creating a task on github or CRM.
- Before creating a event it pings on slack to get user authorization and missing info in case more information is needed.
- Once approved it can directly create bookings or github issues for you.

### Tech Stack
- Python
- OpenAI
- AWS transcribe
- AWS EC2
- Docker

### Getting started 

To run the code, you will need the credentials defined in the `.env` file

Start by running `cp .env.example .env`

You will need the following enironment variables to run the code:

```
CAL_API_KEY=
CAL_API_URL='https://api.cal.com/v1/'
ACCESS_TOKEN=
OPENAI_API_KEY=
OPENAI_ORG_ID=
FLASK_URL=
AWS_ACCESS_KEY=
AWS_SECRET_KEY=
SLACK_HOOK=
SLACK_MEETING_ANALYTICS_HOOK=
CAL_USERNAME=
GITHUB_PAT_TOKEN=
PYTHONPATH=.
```

You can find your OPENAI keys [here](https://platform.openai.com/api-keys)

You can create your AWS access keys using [this document](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)


You can create your own slack webhook following [this link](https://api.slack.com/automation/triggers/webhook)

Once you have the environment variables, you can run the code by running `python main.py`

You will need to provide your AWS S3 `bucket name`
and `object key`. This will be used to access your video or audio file in store in the S3 location

We currently support these file formats ```AMR,FLAC,M4A,MP3,MP4,Ogg,WebM,WAV```

### Running the app

Make sure your S3 bucket and lambda triggers are configured as necessary.

Once you clone the repo
```
cd cal-do-more
sudo docker-compose build
sudo docker-compose up
```

Your api will start running on port 80 on the server and will be exposed to external users.

### S3 Bucket and Lambda Trigger Setup
Create a new lambda function in AWS named `video transcription`. Copy and paste the following code:
```
import json
import os
import urllib3
import json

def lambda_handler(event, context):
    print(json.dumps(event['Records']))
    flask_url = os.environ["FLASK_URL"]

    api_url = flask_url + "/cal/video/transcribe"
    http = urllib3.PoolManager()


    file_name = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
  
    payload = {
        'object_key': file_name,
        'bucket_name': bucket_name
    }
    encoded_data = json.dumps(payload).encode('utf-8')

    
    response = http.request("POST", api_url, body=encoded_data, headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))['json']

    print(data)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
```

### API docs

```
ENDPOINT: /cal/video/transcribe

INPUT: {
    "bucket_name": "",
    "object_key": ""
}
```

Under `Function Overview`, click on the `+ Add trigger` button. 
In `Trigger Configuration`, select `S3` as the source and add the information about the bucket you created. For `Event Types`, select `All Object Create Events`. Click `Add` and this should set up the S3 trigger for your lambda function. 

This will be necessary to hit the transcription endpoint on video upload triggers.

## FUTURE WORK
- Make Prompts more focused to get exact events and ensure we dont miss info
- Add authentication
- Check for cal.com availability and provide prefer times.
- Connect with daily video conferencing used by cal.
- Add meeting analysis like time spent on different topics.
- Add support to whisper for people who dont want to work with aws transcript
- Automatically fetch the cal team and select the participants for the call.
- Synchronize slack assistant events to avoid duplication actions
