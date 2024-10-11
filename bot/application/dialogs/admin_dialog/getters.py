from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from dishka.integrations.aiogram_dialog import inject
from dishka.integrations.aiogram import FromDishka
from fluentogram import TranslatorRunner

from core.enums import LinksRedisKeys
from repository.implementations.common_cache_repository import CommonCacheRepository
from repository.implementations.user_repository import UserRepository

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

@inject
async def common_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        cache: FromDishka[CommonCacheRepository],
        **kwargs
):
    image_id = await cache.get(name=LinksRedisKeys.PHOTO)
    image = None
    if image_id:
        image = MediaAttachment(type=ContentType.PHOTO, file_id=MediaId(image_id))
    return {
        'previous_button': i18n.previous_button(),
        'next_button': i18n.next_button(),
        'skip_button': i18n.skip_button(),
        'image': image,
        'has_image': bool(image)
    }
@inject
async def menu_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        sql_repository: FromDishka[UserRepository],
        cache: FromDishka[CommonCacheRepository],
        **kwargs
):
    users_count = await sql_repository.get_users_count()
    promo_codes_count = await cache.lcount(LinksRedisKeys.PROMO_CODES)
    return {
        'admin_menu_message': i18n.admin_menu.message(users_count=users_count, promo_codes_count=promo_codes_count),
        'setup_personal_cabinet_link_button': i18n.setup_personal_cabinet_link.button(),
        'setup_launcher_links_button': i18n.setup_launcher_links.button(),
        'setup_image_button': i18n.setup_image.button(),
        'setup_promo_codes_button': i18n.setup_promo_codes.button(),
        'mailing_button': i18n.mailing.button(),
    }

async def setup_personal_cabinet_link_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'setup_personal_cabinet_link_message': i18n.setup_personal_cabinet_link.message(),
    }

async def setup_launcher_links_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'setup_launcher_links_message': i18n.setup_launcher_links.message(),
        'yandex_disc_button': i18n.yandex_disc.button(),
        'google_drive_button': i18n.google_drive.button(),
    }

async def setup_image_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'setup_image_message': i18n.setup_image.message(),
    }

async def setup_promo_codes_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'setup_promo_codes_message': i18n.setup_promo_codes.message(),
    }

async def setup_yandex_disc_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'yandex_disc_link_message': i18n.yandex_disc.message()
    }

async def setup_google_drive_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'google_drive_link_message': i18n.google_drive.message()
    }