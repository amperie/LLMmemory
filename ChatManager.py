from ChatGPTBackend import ChatGPTBackend
from LLMMemory import LLMMemory

class ChatManager:
    def __init__(self):
        self._backend = ChatGPTBackend()
        self._memory = LLMMemory(
            host='redis-13783.c98.us-east-1-4.ec2.redns.redis-cloud.com',
            port=13783,
            decode_responses=True,
            username="default",
            password="vhVw1FuYKq6QQ2Enct3G0iJSYrRyA2cY",
    )

    def process_user_message(
            self, user_id, message,
            use_memory: bool = True, mem_length: int = 10
    ) -> str:
        if use_memory:
            mem = self._memory.get_last_n_messages_as_string(user_id, 1, mem_length)
            prompt = f"The following is a conversation between a user and an AI assistant. " \
                "The user is represented by the symbol <USER> and the assistant is represented by the symbol <ASSISTANT>.\n\n" \
                f"Here are the last {mem_length} messages:\n" \
                f"{mem}\n\n" \
                "Here is the new message from the user:\n" \
                f"<USER> {message}\n\n" \
                "Please respond to the user's message based on the conversation history. " \
                "If the user's message is not related to the conversation history, " \
                "please respond with a neutral message."
        else:
            prompt = f"The following is a conversation between a user and an AI assistant. " \
                "The user is represented by the symbol <USER> and the assistant is represented by the symbol <ASSISTANT>.\n\n" \
                "Here is the message from the user:\n" \
                f"<USER> {message}\n\n" \

        msg = [{"role": "user", "content": prompt}]
        response = self._backend.get_response(msg)

        if use_memory:
            self._memory.add_message(user_id, 1, message, "<USER>")
            self._memory.add_message(user_id, 1, response, "<ASSISTANT>")
        return response
        

cm = ChatManager()
response = cm.process_user_message("5", "so how can I solve my problem?", use_memory=False)
print(response)
response = cm.process_user_message("5", "so how can I solve my problem?")
print(response)
pass
