from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from utils.assistants import get_grades
from utils.sql import get_user_token


async def get(user_id):
    kb = InlineKeyboardBuilder()
    grades = await get_grades(await get_user_token(user_id))
    for subject in grades:
        kb.row(InlineKeyboardButton(text=subject['SubjectName']['RU'], callback_data=subject['SubjectID']))
    return kb
