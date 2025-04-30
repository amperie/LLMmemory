from openai import OpenAI
import os


class ChatGPTBackend:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages)
        return response.choices[0].message.content
