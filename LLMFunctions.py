from openai import OpenAI
import os

oai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=oai_api_key)


def get_llm_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages)
    return response.choices[0].message.content


print(get_llm_response([{"role": "user", "content": "What's the capital of France?"}]))
pass
