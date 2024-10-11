from typing import AsyncIterator

import nats
from nats.aio.client import Client
from nats.js import JetStreamContext
from dishka import Provider, provide, Scope
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config.config import get_config, ConfigModel


class BaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> ConfigModel:
        return get_config()

    @provide(scope=Scope.APP)
    async def get_redis(self, config: ConfigModel) -> AsyncIterator[Redis]:
        r = Redis.from_url(config.redis.dsn.unicode_string())
        yield r
        await r.aclose()

    @provide(scope=Scope.APP)
    async def get_sessionmaker(self, config: ConfigModel) -> async_sessionmaker:
        engine = create_async_engine(url=config.db.dsn.unicode_string())
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=True)

    @provide(scope=Scope.REQUEST)
    async def get_db_session(self, sessionmaker: async_sessionmaker) -> AsyncIterator[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    @provide(scope=Scope.APP)
    async def get_nats(self, config: ConfigModel) -> AsyncIterator[Client]:
        nc: Client =  await nats.connect([config.nats.dsn.unicode_string()])
        yield nc
        await nc.close()

    @provide(scope=Scope.APP)
    def get_js(self, nc: Client) -> JetStreamContext:
        js = nc.jetstream()
        return js






