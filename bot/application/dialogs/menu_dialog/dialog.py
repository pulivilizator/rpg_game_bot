from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Url, Start, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format

from application.states import MainMenuSG, AdminSG
from core.enums import Language
from .getters import main_menu_getter, launchers_getter, promo_code_getter
from .handlers import check_subscribe
from ..admin_dialog.getters import common_getter

dialog = Dialog(
    Window(
        DynamicMedia(selector='image', when='has_image'),
        Format('{menu_message}'),
        Url(Format('{personal_cabinet_button}'), url=Format('{personal_cabinet_link}'), when='has_link'),
        SwitchTo(Format('{launcher_button}'), state=MainMenuSG.launcher, id='launcher'),
        SwitchTo(Format('{promo_code_button}'), state=MainMenuSG.promo_code, id='get_promo_code'),
        Url(text=Format('{discord_button}'), url=Format('https://discord.gg/An2mux6pyY')),
        Url(Format('{idea_bot_button}'), url=Format('https://t.me/BAZAFEED_BOT')),
        Start(text=Format('{admin_menu_button}'), state=AdminSG.menu, when='is_admin', id='start_admin_menu'),
        Button(text=Format('{change_lang_button}'), id=Language.WIDGET_KEY),
        getter=main_menu_getter,
        state=MainMenuSG.menu
    ),
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{promo_code_message}'),
        Url(Format('{subscribe_button}'), url=Format('{promo_code_link}'), when='not_subscribe'),
        Button(Format('{subscribe_check_button}'), on_click=check_subscribe, when='not_subscribe', id='check_subscribe'),
        SwitchTo(Format('{previous_button}'), state=MainMenuSG.menu, id='back_to_menu'),
        getter=promo_code_getter,
        state=MainMenuSG.promo_code
    ),
    Window(
DynamicMedia(selector='image', when='has_image'),
        Format('{launcher_message}'),
        Url(Format('{yandex_button}'), url=Format('{yandex_link}'), when='has_yandex'),
        Url(Format('{google_button}'), url=Format('{google_link}'), when='has_google'),
        SwitchTo(Format('{previous_button}'), state=MainMenuSG.menu, id='back_to_menu'),
        getter=launchers_getter,
        state=MainMenuSG.launcher
    ),
    getter=common_getter
)