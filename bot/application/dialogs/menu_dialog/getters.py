from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberLeft
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram_dialog import inject
from dishka.integrations.aiogram import FromDishka
from fluentogram import TranslatorRunner
from sqlalchemy.util import await_only

from core import dto
from core.config.config import ConfigModel
from core.enums import LinksRedisKeys, Language, LanguageList
from repository.implementations.common_cache_repository import CommonCacheRepository
from repository.implementations.user_cache_repository import UserCacheRepository

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

@inject
async def main_menu_getter(dialog_manager: DialogManager,
                           i18n: TranslatorRunner,
                           cache: FromDishka[CommonCacheRepository],
                           user_cache: FromDishka[UserCacheRepository],
                           **kwargs):
    cabinet_link = await cache.get(LinksRedisKeys.PERSONAL_CABINET)
    user = dialog_manager.event.from_user
    is_admin: dto.IsAdmin = await user_cache.hget_all(user_id=user.id, response_model=dto.IsAdmin)

    current_lang: dto.UserLanguage = await user_cache.hget_all(user_id=user.id, response_model=dto.UserLanguage)
    change_lang_button = i18n.lang.russian()
    if current_lang.language == LanguageList.RU:
        change_lang_button = i18n.lang.english()

    return {
        'menu_message': i18n.menu_message(),
        'personal_cabinet_button': i18n.personal_cabinet_button(),
        'personal_cabinet_link': cabinet_link,
        'launcher_button': i18n.launcher.button(),
        'admin_menu_button': i18n.admin_menu_button(),
        'has_link': cabinet_link,
        'is_admin': is_admin.is_admin,
        'change_lang_button': change_lang_button,
        'idea_bot_button': i18n.idea_bot.button(),
        'promo_code_button': i18n.promo_code.button(),
        'discord_button': i18n.discord.button(),
    }

@inject
async def launchers_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    cache: FromDishka[CommonCacheRepository],
    **kwargs
):
    google_link = await cache.get(LinksRedisKeys.LAUNCHER_GOOGLE_DRIVE)
    yandex_link = await cache.get(LinksRedisKeys.LAUNCHER_YANDEX_DISC)

    message = i18n.launcher.message()
    if not google_link and not yandex_link:
        message = i18n.launcher.empty_message()

    return {
        'launcher_message': message,
        'yandex_button': i18n.download_from.yandex.button(),
        'yandex_link': yandex_link,
        'google_link': google_link,
        'google_button': i18n.download_from.google.button(),
        'has_yandex': bool(yandex_link),
        'has_google': bool(google_link)
    }
@inject
async def promo_code_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        config: FromDishka[ConfigModel],
        repository: FromDishka[CommonCacheRepository],
        **kwargs
):
    bot: Bot = dialog_manager.middleware_data.get('bot')
    user = dialog_manager.event.from_user
    is_codes = await repository.exists(LinksRedisKeys.PROMO_CODES)
    if not is_codes:
        return {
            'promo_code_message': i18n.promo_code.empty_message(),
            'promo_code_link': None,
            'subscribe_button': None,
            'subscribe_check_button': None,
            'not_subscribe': False
        }

    used_key = LinksRedisKeys.USER_PROMO_USED.format(user.id)
    if await repository.exists(used_key):
        code = await repository.get(used_key)
        message = i18n.promo_code.used_message(code=code)
        return {
            'promo_code_message': message,
            'promo_code_link': None,
            'subscribe_button': None,
            'subscribe_check_button': None,
            'not_subscribe': False
        }

    user_status = await bot.get_chat_member(chat_id=config.bot.subscribe_group_id,
                                             user_id=user.id)
    not_subscribe = user_status.status == ChatMemberStatus.LEFT
    invite_link = None
    if not_subscribe:
        message = i18n.promo_code.subscribe()
        chat = await bot.get_chat(chat_id=config.bot.subscribe_group_id)
        invite_link = chat.invite_link
    else:
        code = await repository.get_promocode(key=LinksRedisKeys.PROMO_CODES)
        message = i18n.promo_code.message(code=code)
        await repository.set(used_key,
                             value=code)
    return {
        'promo_code_message': message,
        'promo_code_link': invite_link,
        'subscribe_button': i18n.subscribe_button(),
        'subscribe_check_button': i18n.subscribe_check_button(),
        'not_subscribe': not_subscribe
    }