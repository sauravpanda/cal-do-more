import os
import requests
import dateparser

CONTEXT_PL = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "**Potential Meeting:** \n Desc: {text} \n When: {dt}",
    },
}

YES_NO_PL = {
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Create Event", "emoji": True},
            "value": "yes",
            "url": "http://127.0.0.1:5000/response?data=yes",
            "action_id": "actionId-0",
        },
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "No Need", "emoji": True},
            "value": "no",
            "url": "http://127.0.0.1:5000/response?data=no",
            "action_id": "actionId-2",
        },
    ],
}

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
        pass
    else:
        # Ask for approval
        info = info["template_data"]
        dt_str = get_dt_str(info)
        dt = dateparser.parse(dt_str, languages=["en"])
        ctx["text"]["text"] = ctx["text"]["text"].format(
            text=td["summary"], dt=dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        )
        pl = {"blocks": [ctx, YES_NO_PL]}
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

    temp_pl = []
    ctx = CONTEXT_PL
    td = dl["template_data"]

    # dt = dateparser.parse(dt_str, languages=["en"])
    # ctx["text"]["text"] = ctx["text"]["text"].format(
    #     text=td["summary"], dt=dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    # )
    # pl = {"blocks": [ctx, YES_NO_PL]}
    # send_webhook(pl)
