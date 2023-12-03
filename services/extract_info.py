from services.llm import make_oai_call

CATEGORIES = [
    "Future Meeting",
    "Github Issues",
    "Problem-Solving Sessions",
    "Training Session",
    "Product Development",
    "Customer and Client Focus",
    "Quality Assurance",
    "Casual Conversation",
    "Feedback and Open Forums",
    "Research and Development",
]

ACTIONS = ["SETUP A MEETING", "SETUP REMINDER", "Create an ISSUE", "OTHER"]

MEETING_RELATED_CAT = [
    "Future Meeting",
    "Problem-Solving Sessions",
    "Training Session",
    "Customer and Client Focus",
]


def check_if_cal_event_needed(text):
    prompt = f"""
        For given text check if we need to create a calendar event.
        Answer in json format and only return true or false.
        Your output should look like:
        OUTPUT: {{"create_event": true}}

        TEXT: {text}
    """
    res = make_oai_call(prompt)
    return res


def get_event_info(text):
    prompt = f"""
        For given text try to fill the following template.
        If you dont find some info, create a follow up question for that sepcific info
        All output should be in json format.
        Prefer asking questions over guessing answers to template.
        If you dont know the values, fill it as "TBD"

        TEXT: {text}

        TEMPLATE: {{
            "date": <YYYY-MM-DD>,
            "time": <time>,
            "relative_date": <relative_date>,
            "summary: "Text Summary"
        }}

        Your output should look like:
        OUTPUT: {{"template_data": <TEMPLATE_DATA>, "question": "<question>"}}


    """
    res = make_oai_call(prompt)
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
        pass it as a list of dict in json format with the following format:
        OUTPUT: {{
            "data": [
                {{"topic": "TOPIC", "para":"para", "category": "category"}},
                {{"topic": "TOPIC", "para":"para", "category": "category"}}
            ]
        }}

        TEXT: {text}"""

    res = make_oai_call(prompt)
    return res["data"]


def segregate_tasks(results):
    for res in results:
        if res["category"] in MEETING_RELATED_CAT:
            r = check_if_cal_event_needed(res["para"])
            if r["create_event"]:
                info = get_event_info(res["para"])
                info
                # Send a slack ping for this task

    pass


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
    print(
        get_event_info(
            "And next week, we also have a conference coming up. \
            So we need to talk to a few more customers. And we need to \
            identify who the potential customers might be. So maybe let's sit \
            on Monday and try to finalize who are the potential customers. \
            And schedule calls with them."
        )
    )
