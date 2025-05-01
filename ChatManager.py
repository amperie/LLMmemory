from ChatGPTBackend import ChatGPTBackend
from LLMMemory import LLMMemory
import yaml


class ChatManager:
    def __init__(self, config_path: str = "config.yaml"):
        # Load configuration
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        oai_token = config['chat']['openai_token']
        self._backend = ChatGPTBackend(token=oai_token)

        self._memory = LLMMemory(
            host=config['redis']['host'],
            port=config['redis']['port'],
            decode_responses=config['redis']['decode_responses'],
            username=config['redis']['username'],
            password=config['redis']['password'],
            db=config['redis']['db']
        )

        # Store chat configuration
        self._config = config.get('chat', {})
        self._default_user_id = self._config.get('user_id', '1')
        self._default_chat_id = self._config.get('chat_id', 1)
        self._memory_length = self._config.get('memory_length', 10)

    def process_user_message(
            self,
            user_id: str = None, 
            message: str = None,
            use_memory: bool = True,
            mem_length: int = None
    ) -> str:

        user_id = user_id or self._default_user_id
        mem_length = mem_length or self._memory_length

        if use_memory:
            mem = self._memory.get_last_n_messages_as_string(
                user_id, self._default_chat_id, mem_length)
            prompt = f"The following is a conversation between a " \
                "user and an AI assistant. " \
                "The user is represented by the symbol <USER> and the " \
                "assistant is " \
                "represented by the symbol <ASSISTANT>.\n\n" \
                f"Here are the last {mem_length} messages:\n" \
                f"{mem}\n\n" \
                "Here is the new message from the user:\n" \
                f"<USER> {message}\n\n" \
                "Please respond to the user's message based on " \
                "the conversation history. " \
                "If the user's message is not related to the conversation" \
                "history, please respond with a neutral message."
        else:
            prompt = f"The following is a conversation between " \
                "a user and an AI assistant. " \
                "The user is represented by the symbol <USER> and " \
                "the assistant is represented by the symbol <ASSISTANT>.\n\n" \
                "Here is the message from the user:\n" \
                f"<USER> {message}\n\n"

        msg = [{"role": "user", "content": prompt}]
        response = self._backend.get_response(msg)

        self._memory.add_message(
            user_id, self._default_chat_id, message, "<USER>")
        self._memory.add_message(
            user_id, self._default_chat_id, response, "<ASSISTANT>")
        return response


pass
