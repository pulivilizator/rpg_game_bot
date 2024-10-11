import asyncio
from typing import Any

from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject
from nats.js import JetStreamContext

from core import dto
from core.enums import MailingKeys
from repository.implementations.common_cache_repository import CommonCacheRepository
from repository.implementations.user_repository import UserRepository
from services.mailing.publisher import publish_mailing_message


async def save_mailing_text(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str,
):
    dialog_manager.dialog_data.update({MailingKeys.TEXT: text})
    await dialog_manager.next()

async def save_mailing_media(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    file_id = None
    if message.photo:
        file_id = f'{message.photo[1].file_id}:{str(ContentType.PHOTO.value)}'
    file_id = file_id or f'{message.video.file_id}:{str(ContentType.VIDEO.value)}'

    dialog_manager.dialog_data.update({MailingKeys.MEDIA: file_id})
    await dialog_manager.next()


async def save_mailing_links(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str
):
    links = '|'.join([':::'.join(i.rsplit(' ', 1)) for i in text.splitlines()])
    dialog_manager.dialog_data.update({MailingKeys.LINKS: links})
    await dialog_manager.next()

@inject
async def start_mailing(
        message: Message,
        widget: Button,
        dialog_manager: DialogManager,
        cache: FromDishka[CommonCacheRepository],
        user_repository: FromDishka[UserRepository],
        js: FromDishka[JetStreamContext]
):
    await cache.set_ex(name=MailingKeys.TEXT, value=dialog_manager.dialog_data.get(MailingKeys.TEXT), time=int(MailingKeys.EX_TEXT_TIME))
    if media := dialog_manager.dialog_data.get(MailingKeys.MEDIA):
        await cache.set(name=MailingKeys.MEDIA, value=media)
    if links := dialog_manager.dialog_data.get(MailingKeys.LINKS):
        await cache.set(name=MailingKeys.LINKS, value=links)

    await dialog_manager.done()

    users: list[dto.User] = await user_repository.list()

    await asyncio.gather(*[publish_mailing_message(js=js,
                                                 chat_id=user.user_id,
                                                 subject=MailingKeys.SUBJECT,
                                                 delay=0)
                         for i, user in enumerate(users)])
@inject
async def clear_mailing(
        _: Any,
        dialog_manager: DialogManager,
        cache: FromDishka[CommonCacheRepository],
):
    await cache.delete(MailingKeys.MEDIA, MailingKeys.LINKS, MailingKeys.TEXT)