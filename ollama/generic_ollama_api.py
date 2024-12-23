import ollama

model = None # Initialize model as None

def get_ollama_response(model, prompt):

    response = ollama.chat(
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        model=model
    )

    print('Ollama Api Response : ', response['message']['content'])
    return response['message']['content']


model = "llama3.2"
prompt = "Who is APJ Abdul Kalam"
response = get_ollama_response(model, prompt)

