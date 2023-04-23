from aiogram import Router, types
from aiogram.filters import Text

from utils.assistants import get_profile
from states import LoginStateGroup
from utils.sql import get_user_token

router = Router()


@router.message(LoginStateGroup.login, Text('Профиль'))
async def cmd_profile(message: types.Message):
    try:
        profile = await get_profile(await get_user_token(message.from_user.id))
        await message.answer(f"{profile['FullName']['RU']}\n{profile['Specialty']['RU']}\n{profile['Course']} курс")
    except ValueError:
        await message.answer('Произошла ошибка, попробуйте выйти из системы и войти заново')
