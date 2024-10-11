from dishka import Provider, provide, Scope, from_context
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core import dto
from repository.implementations.common_cache_repository import CommonCacheRepository
from repository.implementations.user_cache_repository import UserCacheRepository
from repository.implementations.user_repository import UserRepository
from repository.models import User


class RepositoryProvider(Provider):

    @provide(scope=Scope.APP)
    def get_cache(self, r: Redis) -> UserCacheRepository:
        return UserCacheRepository(r=r)

    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(
            session=session,
            model=User,
            dto_model=dto.User,
            lookup_field='user_id'
        )

    @provide(scope=Scope.APP)
    async def get_user_from_cache(self, r: Redis) -> CommonCacheRepository:
        return CommonCacheRepository(r=r)








