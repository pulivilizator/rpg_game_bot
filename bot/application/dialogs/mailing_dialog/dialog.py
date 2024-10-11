from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Next, Button
from aiogram_dialog.widgets.text import Format

from application.states import MailingSG
from .getters import save_text_getter, save_mailing_media_getter, save_mailing_links_getter, start_mailing_getter
from .handlers import save_mailing_text, save_mailing_media, save_mailing_links, start_mailing, clear_mailing
from ..admin_dialog.filters import link_filter
from ..admin_dialog.getters import common_getter
from ..admin_dialog.handlers import incorrect_input_link

dialog = Dialog(
    Window(
        Format('{save_mailing_text_message}'),
        TextInput(
            on_success=save_mailing_text,
            id='save_mailing_text'
        ),
        Cancel(Format('{previous_button}')),
        getter=save_text_getter,
        state=MailingSG.text
    ),
    Window(
        Format('{save_mailing_media_message}'),
        MessageInput(
            content_types=[ContentType.PHOTO, ContentType.VIDEO],
            func=save_mailing_media,
        ),
        Next(Format('{skip_button}')),
        Back(Format('{previous_button}')),
        getter=save_mailing_media_getter,
        state=MailingSG.media
    ),
    Window(
        Format('{save_mailing_links_message}'),
        TextInput(
            on_success=save_mailing_links,
            id='save_mailing_button_text'
        ),
        Next(Format('{skip_button}')),
        Back(Format('{previous_button}')),
        getter=save_mailing_links_getter,
        state=MailingSG.links
    ),
    Window(
        Format('{start_mailing_message}'),
        Button(text=Format('{start_mailing_button}'), id='start_mailing', on_click=start_mailing),
        Back(Format('{previous_button}')),
        getter=start_mailing_getter,
        state=MailingSG.start_mailing
    ),
    getter=common_getter,
    on_start=clear_mailing
)