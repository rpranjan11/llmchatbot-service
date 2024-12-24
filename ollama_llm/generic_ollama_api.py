import ollama

def get_ollama_generic_response(model, prompt):

    response = ollama.chat(
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        model=model
    )

    return response['message']['content']


# model = "llama3.2"
# prompt = "Who is APJ Abdul Kalam"
# response = get_ollama_response(model, prompt)
# print('Ollama Api Response : ', response)
