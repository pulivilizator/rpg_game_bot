from repository.interfaces.redis_repository import RedisRepository


class CommonCacheRepository(RedisRepository):
    async def set_list(self, key: str, data: list):
        await self.r.rpush(key, *data)

    async def get_promocode(self, key: str, count: int = 1) -> str:
        result = await self.r.rpop(key, count)
        return result[0].decode('utf-8') if result else None

    async def lcount(self, key: str):
        count = await self.r.llen(key)
        return count