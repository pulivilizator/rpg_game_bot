from aiogram.types import TelegramObject, Update, User
from dishka import Provider, provide, Scope, from_context
from fluentogram import TranslatorHub, TranslatorRunner
from sqlalchemy.util import await_only

from core.enums import Language
from infrastructure.utils.i18n import create_translator_hub
from repository.implementations.user_cache_repository import UserCacheRepository


class I18nProvider(Provider):

    @provide(scope=Scope.APP)
    def get_translator_hub(self) -> TranslatorHub:
        translator_hub = create_translator_hub()
        return translator_hub





