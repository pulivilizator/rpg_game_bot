from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import User, TelegramObject
from dishka.integrations.aiogram import FromDishka
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from core import dto
from core.config.config import ConfigModel
from core.enums import Language
from repository.implementations.user_cache_repository import UserCacheRepository
from repository.implementations.user_repository import UserRepository
from .inject_middleware import aiogram_middleware_inject


class RegisterMiddleware(BaseMiddleware):
    @aiogram_middleware_inject
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
            repository: FromDishka[UserCacheRepository],
            sql_repository: FromDishka[UserRepository],
            config: FromDishka[ConfigModel]
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)


        if not await repository.user_exists(user_id=user.id):
            db_user: dto.User | None = await sql_repository.retrieve(user.id, raise_for_none=False)
            if db_user is None:
                is_admin = user.id in config.bot.admins
                new_user = dto.UserBase(
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_admin=is_admin
                )
                db_user = await sql_repository.create(new_user)
            await repository.hset(user_id=user.id, model_data=db_user)




        return await handler(event, data)