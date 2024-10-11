from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel, Start, Back, Next
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format

from application.states import AdminSG, MailingSG
from .filters import link_filter
from .getters import common_getter, menu_getter, setup_image_getter, setup_promo_codes_getter, \
    setup_launcher_links_getter, setup_personal_cabinet_link_getter, setup_google_drive_getter, setup_yandex_disc_getter
from .handlers import incorrect_input_link, setup_personal_cabinet_link, setup_yandex_disc_link, \
    setup_google_drive_link, setup_photo, incorrect_input_image, setup_document

dialog = Dialog(
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{admin_menu_message}'),
        SwitchTo(Format('{setup_personal_cabinet_link_button}'),
                 state=AdminSG.add_personal_cabinet_link,
                 id='setup_personal_cabinet_link'),
        SwitchTo(Format('{setup_launcher_links_button}'),
                 state=AdminSG.add_launcher_links,
                 id='setup_launcher_links'),
        SwitchTo(Format('{setup_image_button}'),
                 state=AdminSG.add_image,
                 id='setup_image'),
        SwitchTo(Format('{setup_promo_codes_button}'),
                 state=AdminSG.add_promo_codes,
                 id='setup_promo_codes'),

        Start(Format('{mailing_button}'), state=MailingSG.text, id='start_mailing'),

        Cancel(Format('{previous_button}')),
        getter=menu_getter,
        state=AdminSG.menu
    ),
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{setup_personal_cabinet_link_message}'),
        TextInput(
            type_factory=link_filter,
            on_success=setup_personal_cabinet_link,
            on_error=incorrect_input_link,
            id='setup_personal_cabinet_link'
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input_link,
        ),
        SwitchTo(Format('{previous_button}'), state=AdminSG.menu, id='back_to_menu'),
        getter=setup_personal_cabinet_link_getter,
        state=AdminSG.add_personal_cabinet_link
    ),
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{setup_launcher_links_message}'),
        SwitchTo(Format('{yandex_disc_button}'), state=AdminSG.yandex_disc_link, id='yandex_disc'),
        SwitchTo(Format('{google_drive_button}'), state=AdminSG.google_drive_link, id='google_drive'),
        SwitchTo(Format('{previous_button}'), state=AdminSG.menu, id='back_to_menu'),
        getter=setup_launcher_links_getter,
        state=AdminSG.add_launcher_links
    ),
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{setup_image_message}'),
        MessageInput(
            content_types=ContentType.PHOTO,
            func=setup_photo
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input_image
        ),
        SwitchTo(Format('{previous_button}'), state=AdminSG.menu, id='back_to_menu'),
        getter=setup_image_getter,
        state=AdminSG.add_image
    ),
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{setup_promo_codes_message}'),
        MessageInput(
            content_types=ContentType.DOCUMENT,
            func=setup_document
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input_image
        ),
        SwitchTo(Format('{previous_button}'), state=AdminSG.menu, id='back_to_menu'),
        getter=setup_promo_codes_getter,
        state=AdminSG.add_promo_codes
    ),
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{yandex_disc_link_message}'),
        TextInput(
            type_factory=link_filter,
            on_success=setup_yandex_disc_link,
            on_error=incorrect_input_link,
            id='setup_yandex_disc_link'
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input_link,
        ),
        SwitchTo(Format('{previous_button}'), state=AdminSG.add_launcher_links, id='back_to_add_launcher_links'),
        getter=setup_yandex_disc_getter,
        state=AdminSG.yandex_disc_link,
    ),
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{google_drive_link_message}'),
        TextInput(
            type_factory=link_filter,
            on_success=setup_google_drive_link,
            on_error=incorrect_input_link,
            id='setup_google_drive_link'
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input_link,
        ),
        SwitchTo(Format('{previous_button}'), state=AdminSG.add_launcher_links, id='back_to_add_launcher_links'),
        getter=setup_google_drive_getter,
        state=AdminSG.google_drive_link,
    ),
    getter=common_getter
)