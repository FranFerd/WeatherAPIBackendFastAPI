import redis, json
from configs.app_settings import settings
from datetime import timedelta
from schemas.cached import CachedResponse
from pydantic import BaseModel
from utils.serialize_for_cache import get_serialized_for_cache
class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )

    def get_json(self, redis_key: str) -> dict | str | None:
        cached_data = self.client.get(redis_key)
        if cached_data:
            try:
                return json.loads(cached_data)
            except json.JSONDecodeError:
                return None
        return None
    
    def get_cached(self, key: str) -> CachedResponse:
        cached = self.get_json(key)
        if cached:
            return CachedResponse(is_cached=True, data=cached)
        return CachedResponse(is_cached=False, data=None)

    def set_json(self, redis_key: str, time: timedelta, value: BaseModel | dict | str) -> None:
        value_to_store = get_serialized_for_cache(value)
        self.client.setex(
            name=redis_key,
            value=json.dumps(value_to_store),
            time=time
        )

redis_service = RedisService()  