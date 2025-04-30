import redis
from datetime import datetime
class LLMMemory:

    _rc: redis.Redis

    def __init__(
            self, host='localhost', port=6379,
            decode_responses=True,
            username=None, password=None,
            db=0):
        self._rc = redis.Redis(
            host=host, port=port,
            decode_responses=decode_responses,
            db=db,
            username=username, password=password
            )

    def add(self, user_id, chat_id, message, role):
        msg = {
            "role": role,
            "chat_id": chat_id,
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        self._rc.hset(
            f"messages:{user_id}",
            mapping=msg
        )

    def get(self, user_id, chat_id):
        retVal = self._rc.hgetall(f"messages:{user_id}")
        return retVal


lm = LLMMemory(
    host='redis-13783.c98.us-east-1-4.ec2.redns.redis-cloud.com',
    port=13783,
    decode_responses=True,
    username="default",
    password="vhVw1FuYKq6QQ2Enct3G0iJSYrRyA2cY",
)

lm.add(
    user_id="2",
    chat_id="1",
    message="Hello, how are you?",
    role="user"
)
lm.add(
    user_id="3",
    chat_id="1",
    message="I'm fine, thank you!",
    role="assistant"
)

g = lm.get(user_id="2", chat_id="1")

pass