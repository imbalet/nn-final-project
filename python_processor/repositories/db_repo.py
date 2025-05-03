from dataclasses import asdict
import json
from redis.asyncio import Redis
from repositories import BaseRepo
from schemas import Task
from schemas import Result

GET_TASK_SCRIPT = """
local task_id = redis.call('LPOP', KEYS[1])
if not task_id then
    return nil
end

local url = redis.call('HGET', KEYS[2], task_id)
if not url then
    return nil
end

redis.call('HDEL', KEYS[2], task_id)
redis.call('SADD', KEYS[3], task_id)
return { task_id, url }
"""

SET_RESULT_SCRIPT = """
redis.call('RPUSH', KEYS[1], ARGV[1])
redis.call('SREM', KEYS[2], ARGV[2])
"""


class RedisRepo(BaseRepo):
    def __init__(
        self,
        host: str,
        port: str,
        password: str,
        queue_key: str,
        hash_key: str,
        processing_key: str,
        done_key: str,
    ) -> None:
        self.queue_key = queue_key
        self.hash_key = hash_key
        self.processing_key = processing_key
        self.done_key = done_key

        self.connection: Redis = RedisRepo._connect_redis(
            host=host, port=port, password=password
        )

        self.get_data_script = self.connection.register_script(GET_TASK_SCRIPT)
        self.set_result_script = self.connection.register_script(SET_RESULT_SCRIPT)

    @staticmethod
    def _connect_redis(host: str, port: str, password: str) -> Redis:
        return Redis(host=host, port=port, password=password)

    async def close(self) -> None:
        self.connection.delete("processing")
        await self.connection.close()

    async def get_task(self) -> Task | None:
        data = await self.get_data_script(
            keys=[self.queue_key, self.hash_key, self.processing_key]
        )
        if data is None:
            return None

        if len(data) != 2:
            raise ValueError("Redis return wrong data count")

        task = Task(
            id=data[0].decode(),
            url=data[1].decode(),
        )
        return task

    async def set_result(self, result: Result) -> None:
        dct = asdict(result)
        json_data = json.dumps(dct)
        await self.set_result_script(
            keys=[self.done_key, self.processing_key],
            args=[json_data, result.id],
        )
