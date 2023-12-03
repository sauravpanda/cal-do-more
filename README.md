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