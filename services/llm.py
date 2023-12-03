import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

client = openai.OpenAI(
  organization=os.environ["OPENAI_ORG_ID"],

)

def make_oai_call(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.6,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a Meeting assistant which reviews the meeting notes and make actionable items and summaries."},
            {"role": "user", "content": prompt}
        ],
        
    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    prompt = "Whats the value of pi?"
    print(make_oai_call(prompt))