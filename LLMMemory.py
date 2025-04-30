import redis
import time
import json
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.field import TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import redis.exceptions


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

    def _get_next_sequence_id(self, user_id):
        query = Query(
            f"@user_id:{user_id}"
            ).sort_by("sequence_id", asc=False)
        res = self._rc.ft("idx:messages").search(query)
        if len(res.docs) > 0:
            return json.loads(res.docs[0].json)["sequence_id"] + 1
        else:
            return 1

    def _get_from_index(self, user_id, chat_id, start_seq_id, end_seq_id):
        query = Query(
            f"@user_id:{user_id} "
            f"@chat_id:[{chat_id} {chat_id}] "
            f"@sequence_id:[{start_seq_id} {end_seq_id}]"
            ).sort_by("sequence_id", asc=False)
        retVal = self._rc.ft("idx:messages").search(query)
        return retVal

    def clear_all_memory(self):
        self._rc.ft("idx:messages").dropindex(delete_documents=True)

    def initialize_memory(self):
        try:
            self.clear_all_memory()
        except redis.exceptions.ResponseError:
            pass
        schema = (
            TextField("$.role", as_name="role"),
            TextField("$.user_id", as_name="user_id"),
            NumericField("$.chat_id", as_name="chat_id"),
            TextField("$.content", as_name="content"),
            NumericField("$.timestamp", as_name="timestamp"),
            NumericField("$.sequence_id", as_name="sequence_id"),
        )

        self._rc.ft("idx:messages").create_index(
            schema,
            definition=IndexDefinition(
                prefix=["messages:"], index_type=IndexType.JSON
            )
        )

    def add_message(self, user_id, chat_id, message, role):
        seq_id = self._get_next_sequence_id(user_id)

        msg = {
            "role": role,
            "user_id": user_id,
            "chat_id": chat_id,
            "content": message,
            "timestamp": int(time.time()),
            "sequence_id": seq_id,
        }
        self._rc.json().set(
            f"messages:user_id_{user_id}_seq_{seq_id}",
            Path.root_path(),
            msg)

    def get_last_n_messages(self, user_id, chat_id, n):
        curr_seq = self._get_next_sequence_id(user_id) - 1
        start_seq = max(0, curr_seq-n)
        res = self._get_from_index(user_id, chat_id, start_seq, curr_seq)
        retVal = [json.loads(doc.json) for doc in res.docs]
        return retVal

    def get_last_n_messages_as_string(self, user_id, chat_id, n):
        retVal = self.get_last_n_messages(user_id, chat_id, n)
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in retVal])

pass
