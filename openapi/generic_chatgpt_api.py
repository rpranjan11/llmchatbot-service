from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAPI_API_KEY')
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



# prompt = "Who is Ram Pratap Ranjan"
# response = get_chatgpt_summary(prompt)
