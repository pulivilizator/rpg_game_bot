from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from application.states import MainMenuSG

router = Router()

@router.message(CommandStart())
async def start_process(message: Message,
                        dialog_manager: DialogManager,):
    await dialog_manager.start(state=MainMenuSG.menu, mode=StartMode.RESET_STACK)
