from llm import make_oai_call

CATEGORIES = [
    "Event Planning and Coordination",
    "Project Updates",
    "Strategic Planning",
    "Team Management",
    "Problem-Solving Sessions",
    "Training Session",
    "Product Development",
    "Operational Efficiency",
    "Financial Reviews",
    "Customer and Client Focus",
    "Technology and Innovation",
    "Quality Assurance",
    "Health and Safety",
    "Marketing and Sales",
    "Corporate Governance",
    "Casual Conversation",
    "Sustainability and Social Responsibility",
    "Diversity and Inclusion",
    "Feedback and Open Forums",
    "Research and Development",
]

ACTIONS = [
    "SETUP A MEETING",
    "SETUP REMINDER",
    "Create an ISSUE",
    "OTHER"
]



def get_topics(filename: str):
    '''
        Idea is to get topics in a transcription and return them as a list of items.
    '''
    with open(filename, 'r') as f:
        text = f.read()

    prompt = f'''
        For the given text below identify the topics being discussed in this meeting.
        Merge the topics which are similar.
        Categorize the topics into one of the following: {CATEGORIES}
        pass it as a list of dict in json format with the following format:

        OUTPUT: [{{"topic": "TOPIC", "description":"DESC", "category": "category"}}, 
                {{"topic": "<TOPIC>", "description":"<DESC>", "category": "category"}}]

        TEXT: {text}'''

    res = make_oai_call(prompt)
    return res

if __name__== "__main__":
    print(get_topics("sample_data/transcription_1.txt"))