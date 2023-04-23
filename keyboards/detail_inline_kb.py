from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text='Вернуться к списку', callback_data='go_back')
    )
    return kb
