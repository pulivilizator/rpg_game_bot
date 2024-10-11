from aiogram import Router
from .handlers.commands_handler import router as commands_router
from .dialogs import menu_dialog, admin_dialog, mailing_dialog

def get_routers() -> list[Router]:
    return [
        commands_router,
        menu_dialog,
        admin_dialog,
        mailing_dialog,
    ]