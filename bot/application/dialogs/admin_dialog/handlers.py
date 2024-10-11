from io import BytesIO

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from dishka.integrations.aiogram_dialog import inject
from dishka.integrations.aiogram import FromDishka
from fluentogram import TranslatorRunner

from application.states import AdminSG
from core.enums import LinksRedisKeys
from repository.implementations.common_cache_repository import CommonCacheRepository


@inject
async def setup_personal_cabinet_link(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str,
        cache: FromDishka[CommonCacheRepository]
):
    await cache.set(name=LinksRedisKeys.PERSONAL_CABINET, value=text)
    await dialog_manager.switch_to(state=AdminSG.menu)

@inject
async def setup_yandex_disc_link(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str,
        cache: FromDishka[CommonCacheRepository]
):
    await cache.set(name=LinksRedisKeys.LAUNCHER_YANDEX_DISC, value=text)
    await dialog_manager.switch_to(state=AdminSG.add_launcher_links)

@inject
async def setup_google_drive_link(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str,
        cache: FromDishka[CommonCacheRepository]
):
    await cache.set(name=LinksRedisKeys.LAUNCHER_GOOGLE_DRIVE, value=text)
    await dialog_manager.switch_to(state=AdminSG.add_launcher_links)

async def incorrect_input_link(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
        err: Exception | None = None,
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(i18n.incorrect.link.message())
async def incorrect_input_image(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(i18n.incorrect.photo.message())

@inject
async def setup_photo(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
        cache: FromDishka[CommonCacheRepository]
):
    photo_id = message.photo[1].file_id
    await cache.set(name=LinksRedisKeys.PHOTO, value=photo_id)
    await dialog_manager.switch_to(state=AdminSG.menu)

@inject
async def setup_document(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
        cache: FromDishka[CommonCacheRepository]
):
    bot: Bot = dialog_manager.middleware_data.get('bot')
    document = message.document
    file = await bot.get_file(document.file_id)
    file_data = await bot.download_file(file.file_path)
    file_bytes = BytesIO(file_data.read())
    file_content = file_bytes.read().decode('utf-8')
    promo_codes = [i.strip('/|\\ ') for i in file_content.split('\n') if i]
    await cache.set_list(LinksRedisKeys.PROMO_CODES, promo_codes)

    await dialog_manager.switch_to(state=AdminSG.menu)