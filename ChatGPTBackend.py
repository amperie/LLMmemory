from openai import OpenAI
import os


class ChatGPTBackend:
    def __init__(self, token):
        self.client = OpenAI(api_key=token)

    def get_response(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages)
        return response.choices[0].message.content
