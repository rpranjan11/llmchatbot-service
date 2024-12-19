from openai import OpenAI

client = OpenAI(
    api_key = "sk-proj-oxpnb3tt8tyv1UePIiw0T3BlbkFJVlcvRjrKh6JcGyxK1Edx" # "api_key need to be submitted here"
)

model = "gpt-3.5-turbo"

def get_chatgpt_summary(prompt):

    response = client.chat.completions.create(
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        model=model
    )

    print('Chatgpt Api Response : ', response.choices[0].message.content)
    return response.choices[0].message.content



prompt = "Who is Ram Pratap Ranjan"
response = get_chatgpt_summary(prompt)
