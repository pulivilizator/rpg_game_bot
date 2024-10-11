from aiogram.fsm.state import StatesGroup, State

class MainMenuSG(StatesGroup):
    menu = State()
    launcher = State()
    promo_code = State()

class AdminSG(StatesGroup):
    menu = State()
    add_personal_cabinet_link = State()
    add_image = State()
    add_promo_codes = State()
    add_launcher_links = State()
    yandex_disc_link = State()
    google_drive_link = State()
    add_groups = State()
    mailing = State()

class MailingSG(StatesGroup):
    text = State()
    media = State()
    links = State()
    start_mailing = State()