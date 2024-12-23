from openai import OpenAI
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

ASSISTANT_ID = os.getenv('OPENAPI_ASSISTANT_ID')
client = OpenAI(
    api_key=os.getenv('OPENAPI_API_KEY')
)

def get_chatgpt_response_with_file(file):
    
    # Create a vector store called "Supporting Data Files"
    vector_store = client.beta.vector_stores.create(name="Supporting Data Files")
    
    # Ready the files for upload to OpenAI 
    file_paths = [file]
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Use the upload_and_poll SDK helper to upload the file, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    assistant = client.beta.assistants.update(
        assistant_id=ASSISTANT_ID,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    # Upload the user provided file to OpenAI
    message_file = client.files.create(
        file=open(file, "rb"), purpose="assistants"
    )

    # Create a thread with a message.
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Write a brief summary of the content from the file uploaded now",
                "attachments": [
                    { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
                ],
            }
        ]
    )

    # Submit the thread to the assistant (as a new run).
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print(f"Run Created: {run.id}")

    # Wait for run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run Status: {run.status}")
        time.sleep(1)
    else:
        print(f"Run Completed!")

    # Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message = messages[0].content[0].text.value

    return latest_message


def get_chatgpt_response(prompt):

    # Create a thread with a message.
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    # Submit the thread to the assistant (as a new run).
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print(f"Run Created: {run.id}")

    # Wait for run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run Status: {run.status}")
        time.sleep(1)
    else:
        print(f"Run Completed!")

    # Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message = messages[0].content[0].text.value

    return latest_message




file = "./PDFfiles/Ranjan.pdf"
prompt = "Who is Ranjan"
response = get_chatgpt_response(prompt)
print(response)
print('----------------------------------')
response = get_chatgpt_response_with_file(file)
print(response)
print('----------------------------------')
response = get_chatgpt_response(prompt)
print(response)
