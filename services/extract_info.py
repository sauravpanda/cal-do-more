from services.llm import make_oai_call

CATEGORIES = [
    "Event Planning and Coordination",
    "Project Updates",
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


def get_topics(text):
    """
    Idea is to get topics in a transcription and return them as a list of items.
    """
    if type(text) != str:
        res = ""
        for item in text:
            res += f"{item['speaker']}: {item['speech']} \n"
        text = res

    prompt = f"""
        For the given text below identify the topics being discussed in this meeting.
        Categorize the topics into one of the following: {CATEGORIES}
        pass it as a list of dict in json format with the following format:
        OUTPUT: [{{"topic": "TOPIC", "para":"para", "category": "category"}},
                {{"topic": "TOPIC", "para":"para", "category": "category"}}]

        TEXT: {text}"""

    res = make_oai_call(prompt)
    return res


if __name__ == "__main__":
    print(
        get_topics(
            """
            Hi team, how's it going? It's going good, how are you? It's good, good.\
            Let's jump into stand-up. I can go first. \
            So for my part, I worked on the prompt part of the AI.\
            I also wrote a Flask server to expose a few endpoints. \
            You can move my Jira ticket to in-progress. \
            Okay, I'll make the changes. And in the endpoint part, do you remember that bug?\
            Were you able to fix it on your own? No, I think I'll need to connect with you later on. \
            Okay, why don't we connect tomorrow at 4pm?\
            Okay, tomorrow 4pm sounds good. I'll also have to loop in Riddhima. \
            So I'll see when she's free. She should also mostly be free after 3.\
            So 4pm should work for all of us. Okay, sounds good. And I also had this new issue pop-up from customer.\
            And they were mentioning the AI is not able to distinguish properly between the two prompts.\
            I think we need to add that to GitHub issues.\
            Can you work on it once you're free? Yep, I'll create a GitHub issue later on in the day. \
            Maybe around noon or something. Okay, makes sense.\
            And next week, we also have a conference coming up. So we need to talk to a few more customers.\
            And we need to identify who the potential customers might be.\
            So maybe let's sit on Monday and try to finalize who are the potential customers.\
            And schedule calls with them. Yeah, sounds good. Okay, cool.\
            Saurav, I'll talk to you later then. Okay, awesome, Parthit. Great job. Bye-bye. Bye-bye.
        """
        )
    )
