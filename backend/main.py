# import ollama
#
# stream = ollama.chat(
#     model='llama2',
#     messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
#     stream=True,
# )
#
# for chunk in stream:
#     print(chunk['message']['content'], end='', flush=True)

# create API that takes in user input and returns a response

import ollama


def get_response(user_input):
    stream = ollama.chat(
        model='llama2',
        messages=[{'role': 'user', 'content': user_input}],
        stream=True,
    )
    for chunk in stream:
        yield chunk['message']['content']
