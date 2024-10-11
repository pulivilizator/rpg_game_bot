from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

async def save_text_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'save_mailing_text_message': i18n.mailing.save_text.message(),
    }

async def save_mailing_media_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'save_mailing_media_message': i18n.mailing.save_media.message(),
    }

async def save_mailing_links_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'save_mailing_links_message': i18n.mailing.save_links.message(),
    }

async def start_mailing_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs
):
    return {
        'start_mailing_message': i18n.mailing.start.message(),
        'start_mailing_button': i18n.mailing.start.button(),

    }