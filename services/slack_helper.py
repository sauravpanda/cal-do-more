import os
import requests
import dateparser
import json

CONTEXT_PL = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Found Potential Meeting:* \n\n *Summary:* {text} \n\n {dt}",
    },
}

GITHUB_CONTEXT_PL = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Creating Github Issue:* \n\n *Desc:* {text} \n\n {dt}",
    },
}

CREATE_EVENT_PL = '''{
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Create Event", "emoji": true},
            "value": "yes",
            "url": "http://127.0.0.1:5000/response?data=yes&type=event&{pl_data}",
            "action_id": "actionId-0"
        },
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "No Need", "emoji": true},
            "value": "no",
            "url": "http://127.0.0.1:5000/response?data=no&type=event&{pl_data}",
            "action_id": "actionId-2"
        }
    ]
}'''

CREATE_ISSUE_PL = '''{
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Create", "emoji": true},
            "value": "yes",
            "url": "http://127.0.0.1:5000/response?data=yes&type=issue&{pl_data}",
            "action_id": "actionId-0"
        },
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "No Need", "emoji": true},
            "value": "no",
            "url": "http://127.0.0.1:5000/response?data=no&type=issue&{pl_data}",
            "action_id": "actionId-2"
        }
    ]
}'''

SETUP_EVENT = '''{
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Setup Cal Event Manually", "emoji": true},
            "value": "yes",
            "url": "https://cal.com/{username}/30min?notes={notes}&date=2023-12-04&month=2023-12",
            "action_id": "actionId-0"
        }
    ]
}'''

QUESTION_PL = {}


def send_webhook(payload):
    slack_webhook_url = os.getenv("SLACK_HOOK")

    # Make the POST request to the Slack incoming webhook URL
    response = requests.post(slack_webhook_url, json=payload)

    # Check the response status
    if response.status_code == 200:
        print("Question sent successfully.")
    else:
        print(
            f"Error sending question to Slack: {response.status_code}, {response.text}"
        )


def get_dt_str(td):
    dt_str = ""

    if td["date"] != "TBD":
        dt_str += f'{td["date"]} '
    if td["time"] != "TBD":
        dt_str += f'{td["time"]} '
    if td["relative_date"]:
        dt_str += td["relative_date"]
    dt_str = dt_str.replace("next", "")
    return dt_str


def get_user_approval(info):
    if info["question"]:
        # Ask a question to user
        td = info["template_data"]
        ctx = CONTEXT_PL
        ctx["text"]["text"] = ctx["text"]["text"].format(
            text=td["summary"],
            dt=info["question"] + "?"
        )
        setup = SETUP_EVENT.replace('{username}', os.environ["CAL_USERNAME"])
        pl = {"blocks": [ctx, json.loads(setup)]}
        print(json.dumps(pl))
        send_webhook(pl)

    else:
        # Ask for approval
        td = info["template_data"]
        dt_str = get_dt_str(td)
        dt = dateparser.parse(dt_str, languages=["en"])
        ctx = CONTEXT_PL
        ctx["text"]["text"] = ctx["text"]["text"].format(
            text=td["summary"],
            dt="When: " + dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        )
        pl_event = CREATE_EVENT_PL.replace(
            "{pl_data}",
            f"time={dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')}&summary={requests.utils.quote(td['summary'])}")
        pl = {"blocks": [ctx, json.loads(pl_event)]}
        print(json.dumps(pl))
        send_webhook(pl)


def get_user_approval_for_github(info):
    # Ask a question to user
    td = info["template_data"]
    ctx = GITHUB_CONTEXT_PL
    ctx["text"]["text"] = ctx["text"]["text"].format(
        text=td["title"],
        dt=td["description"]
    )
    setup = CREATE_ISSUE_PL.replace(
        '{pl_data}',
        f'title={requests.utils.quote(td["title"])}&desc={requests.utils.quote(td["description"])}')
    pl = {"blocks": [ctx, json.loads(setup)]}
    send_webhook(pl)


if __name__ == "__main__":
    dl = {
        "template_data": {
            "date": "TBD",
            "time": "TBD",
            "relative_date": "next Monday",
            "summary": "Identify potential customers and schedule calls with them",
        },
        "question": "What is the specific date and time for the meeting next week to finalize potential customers?",
    }

    dl = {
        "template_data": {
            "date": "TBD",
            "time": "10:00 am",
            "relative_date": "Monday",
            "summary": "Identify potential customers and schedule calls with them",
        },
        "question": "",
    }

    # dl = {
    #     "template_data": {
    #         "title": "New Issue",
    #         "description": "This is a new issue test",
    #     },
    # }

    # temp_pl = []
    # ctx = CONTEXT_PL
    # td = dl["template_data"]
    get_user_approval(dl)
    # get_user_approval_for_github(dl)

    # dt = dateparser.parse(dt_str, languages=["en"])
    # ctx["text"]["text"] = ctx["text"]["text"].format(
    #     text=td["summary"], dt=dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    # )
    # pl = {"blocks": [ctx, YES_NO_PL]}
    # send_webhook(pl)
    # send_webhook(pl)
