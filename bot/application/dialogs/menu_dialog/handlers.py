from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram_dialog import inject


@inject
async def check_subscribe(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        **kwargs
):
    await callback.answer()