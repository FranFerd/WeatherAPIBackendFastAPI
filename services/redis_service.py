import redis.asyncio as redis_async, json

from datetime import timedelta

from schemas.cached import CachedResponse

from pydantic import BaseModel

from configs.app_settings import settings

from utils.serialize_for_cache import get_serialized_for_cache

from fastapi import HTTPException, status

class RedisService:
    MAX_ATTEMPTS = 5
    BLOCK_TIME = 60
    PREFIX = "login_fail"

    def __init__(self):
        self.client = redis_async.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )

    def _get_key(self, username: str) -> str: # _ indicates a private method. Internal logic, not for outside calls.
        return f"{self.PREFIX}:{username}"

    async def get_json(self, redis_key: str) -> dict | str | None:
        cached_data = await self.client.get(redis_key)
        if cached_data:
            try:
                return json.loads(cached_data)
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_cached(self, key: str) -> CachedResponse:
        cached = await self.get_json(key)
        if cached:
            return CachedResponse(is_cached=True, data=cached)
        return CachedResponse(is_cached=False, data=None)

    async def set_json(self, redis_key: str, time: timedelta, value: BaseModel | dict | str) -> None:
        value_to_store = get_serialized_for_cache(value)
        await self.client.setex(
            name=redis_key,
            value=json.dumps(value_to_store),
            time=time
        )

    async def is_blocked(self, username: str) -> None:
        key = self._get_key(username)
        attempts = await self.client.get(key)
        if attempts and int(attempts) > self.MAX_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Try again later"
            )
    
    async def register_failed_attempt(self, username: str) -> None:
        key = self._get_key(username)
        attempts = await self.client.incr(key) #incr sets key to 1 if no key exists
        if attempts == 1: 
             await self.client.expire(key, self.BLOCK_TIME) # sets expiry to attempts immediately, not when blocked

    async def reset_attempts(self, username: str) -> None:
        key = self._get_key(username)
        await self.client.delete(key)

redis_service = RedisService()  