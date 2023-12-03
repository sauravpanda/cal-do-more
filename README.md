# cal-do-more
A Video transcription service for Cal.com meetings

### The Idea:

We take the video, transcribe it, and then process it for potential actions

We use the transcription to identify potential tasks, summaries, and takeaways.

Add follow-up to the discussion.

Add to-do list schedule.


### Getting started 

To run the code, you will need the credentials defined in the `.env` file

Start by running `cp .env.example .env`

You will need the following enironment variables to run the code:

```
OPENAI_ORG_ID=
OPENAI_API_KEY=
AWS_ACCESS_KEY=
AWS_SECRET_KEY=
SLACK_HOOK=
```

You can find your OPENAI keys [here](https://platform.openai.com/api-keys)

You can create your AWS access keys using [this document](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)


You can create your own slack webhook following [this link](https://api.slack.com/automation/triggers/webhook)

Once you have the environment variables, you can run the code by running `python main.py`

You will need to provide your AWS S3 `bucket name`
and `object key`. This will be used to access your audio file in store in the S3 location