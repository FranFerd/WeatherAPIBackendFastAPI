import redis, json
from configs.app_settings import settings
from datetime import timedelta

class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )

    def get_json(self, redis_key: str) -> dict | None:
        cached_data = self.client.get(redis_key)
        if cached_data:
            try:
                return json.loads(cached_data)
            except json.JSONDecodeError:
                return None
        return None

    def set_json(self, redis_key: str, time: timedelta, value: str):
        self.client.setex(
            name=redis_key,
            value=json.dumps(value),
            time=time
        )

redis_service = RedisService()