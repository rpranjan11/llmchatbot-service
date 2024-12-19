import ollama

model = "llama2"

def get_ollamallm_response(prompt):

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


# prompt = "Who is Ram Pratap Ranjan"
# response = get_ollamallm_response(prompt)

