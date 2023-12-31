from services.llm import make_oai_call
from services.slack_helper import get_user_approval, get_user_approval_for_github
import json
CATEGORIES = [
    "Future Meeting",
    "Github Issues",
    # "Problem-Solving Sessions",
    # "Training Session",
    "Product Development",
    "Customer and Client Focus",
    # "Quality Assurance",
    "Casual Conversation",
    # "Feedback and Open Forums",
    # "Research and Development",
]

ACTIONS = ["SETUP A MEETING", "SETUP REMINDER", "Create an ISSUE", "OTHER"]

MEETING_RELATED_CAT = [
    "Future Meeting",
    "Problem-Solving Sessions",
    "Training Session",
    "Customer and Client Focus",
]

ISSUE_RELATED_CAT = [
    "Product Development",
    # "Training Session",
    "Github Issues",
    "Problem-Solving Sessions",
    "Quality Assurance",
    # "Feedback and Open Forums",
    # "Research and Development",
]


def check_if_cal_event_needed(text):
    prompt = f"""
        For given text check if we need to create a calendar event.
        Answer in json format and only return true or false.
        Your output should look like:
        OUTPUT: {{"create_event": true}}

        TEXT: {text}
    """
    res = json.loads(make_oai_call(prompt))
    return res


def check_github_issue_needed(text):
    prompt = f"""
        For given text check if we need to create a Github issue.
        Answer in json format and only return true or false.
        Your output should look like:
        OUTPUT: {{"create_issue": true}}

        TEXT: {text}
    """
    res = json.loads(make_oai_call(prompt))
    return res


def get_event_info(text):
    prompt = f"""
        For the given text, try to fill out the following template.
        If you don't find some info, create a follow-up question for that specific info
        All output should be in JSON format.
        If you know the date and time, don't ask questions.
        If it's a relative date, just get the close date; there is no need for the exact date.
        If you don't know the values, fill it as "TBD".

        TEXT: {text}

        TEMPLATE: {{
            "date": <YYYY-MM-DD>,
            "time": <time>,
            "relative_date": <relative_date>,
            "summary: "Associated Text"
        }}

        For summary, try to write in third person without using names.

        Your output should look like:
        OUTPUT: {{"template_data": <TEMPLATE_DATA>, "question": "<question>"}}


    """
    res = json.loads(make_oai_call(prompt))
    return res


def get_issue_info(text):
    prompt = f"""
        For the given text, try to fill out the following template.
        If you don't find some info, create a follow-up question for that specific info
        All output should be in JSON format.

        TEXT: {text}

        TEMPLATE: {{
            "title": "",
            "description": ""
        }}

        For description, try to write in third person without using names.

        Your output should look like:
        OUTPUT: {{"template_data": <TEMPLATE_DATA>}}
    """
    res = json.loads(make_oai_call(prompt))
    return res


def get_topics(text):
    """
    Idea is to get topics in a transcription and return them as a list of items.
    """
    if type(text) is not str:
        res = ""
        for item in text:
            res += f"{item['speaker']}: {item['speech']} \n"
        text = res

    prompt = f"""
        For the given text below identify the topics being discussed in this meeting.
        Categorize the topics into one of the following: {CATEGORIES}
        Give the output in json format as shown below:
        OUTPUT: {{
            "data": [
                {{"topic": "TOPIC", "para":"para", "category": "category"}},
                {{"topic": "TOPIC", "para":"para", "category": "category"}}
            ]
        }}

        TEXT: {text}"""

    res = make_oai_call(prompt)
    res = json.loads(res)
    with open('output/topic_results.json', 'w+') as f:
        f.write(json.dumps(res["data"]))
    return res["data"]


def segregate_tasks(results):
    for res in results:
        if res["category"] in MEETING_RELATED_CAT:
            print("Creating meeting")
            r = check_if_cal_event_needed(res["para"])
            if r["create_event"]:
                print("Need to create a event")
                info = get_event_info(res["para"])
                get_user_approval(info)
                continue
                # Send a slack ping for this task
        if res["category"] in ISSUE_RELATED_CAT:
            print("Creating Github Issue")
            r = check_github_issue_needed(res["para"])
            if r["create_issue"]:
                info = get_issue_info(res["para"])
                get_user_approval_for_github(info)


def cal_event():
    pass


if __name__ == "__main__":
    # res = get_topics(
    #         """
    #         Hi team, how's it going? It's going good, how are you? It's good, good.\
    #         Let's jump into stand-up. I can go first. \
    #         So for my part, I worked on the prompt part of the AI.\
    #         I also wrote a Flask server to expose a few endpoints. \
    #         You can move my Jira ticket to in-progress. \
    #         Okay, I'll make the changes. And in the endpoint part, do you remember that bug?\
    #         Were you able to fix it on your own? No, I think I'll need to connect with you later on. \
    #         Okay, why don't we connect tomorrow at 4pm?\
    #         Okay, tomorrow 4pm sounds good. I'll also have to loop in Riddhima. \
    #         So I'll see when she's free. She should also mostly be free after 3.\
    #         So 4pm should work for all of us. Okay, sounds good. And I also had this new issue pop-up from customer.\
    #         And they were mentioning the AI is not able to distinguish properly between the two prompts.\
    #         I think we need to add that to GitHub issues.\
    #         Can you work on it once you're free? Yep, I'll create a GitHub issue later on in the day. \
    #         Maybe around noon or something. Okay, makes sense.\
    #         And next week, we also have a conference coming up. So we need to talk to a few more customers.\
    #         And we need to identify who the potential customers might be.\
    #         So maybe let's sit on Monday and try to finalize who are the potential customers.\
    #         And schedule calls with them. Yeah, sounds good. Okay, cool.\
    #         Saurav, I'll talk to you later then. Okay, awesome, Parthit. Great job. Bye-bye. Bye-bye.
    #     """
    #     )
    # print("res: ", res)
    # print(
    #     get_event_info(
    #         "And next week, we also have a conference coming up. \
    #         So we need to talk to a few more customers. And we need to \
    #         identify who the potential customers might be. So maybe let's sit \
    #         on Monday and try to finalize who are the potential customers. \
    #         And schedule calls with them."
    #     )
    # )

    # print(get_issue_info("And next week, we also have a conference coming up. \
    #          So we need to talk to a few more customers. And we need to \
    #          identify who the potential customers might be. So maybe let's sit \
    #          on Monday and try to finalize who are the potential customers. \
    #          And schedule calls with them."))
    pass
