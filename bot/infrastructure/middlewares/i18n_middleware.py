from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import User, TelegramObject
from dishka.integrations.aiogram import FromDishka
from fluentogram import TranslatorHub

from core import dto
from core.enums import Language, LanguageList
from repository.implementations.user_cache_repository import UserCacheRepository
from repository.implementations.user_repository import UserRepository
from .inject_middleware import aiogram_middleware_inject


class TranslatorRunnerMiddleware(BaseMiddleware):
    @aiogram_middleware_inject
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
            hub: FromDishka[TranslatorHub],
            repository: FromDishka[UserCacheRepository],
            sql_repository: FromDishka[UserRepository]
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        lang = await self._get_lang(event, user, repository, sql_repository)
        data['i18n'] = hub.get_translator_by_locale(lang)
        return await handler(event, data)

    @staticmethod
    async def _get_lang(event: TelegramObject, user: User, repository: UserCacheRepository, sql_repository: UserRepository) -> str:
        current_lang: dto.UserLanguage = await repository.hget_all(user_id=user.id, response_model=dto.UserLanguage)
        if event.callback_query and Language.WIDGET_KEY in event.callback_query.data:
            new_lang = dto.UserLanguage(
                language=LanguageList.EN
                if current_lang.language == LanguageList.RU
                else LanguageList.RU
            )

            await repository.hset(user_id=user.id, model_data=new_lang)
            await sql_repository.update(lookup_value=user.id, update_data=new_lang)
            return new_lang.language
        return current_lang.language