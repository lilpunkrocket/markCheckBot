from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from keyboards import main_menu_kb, login_kb
from states import LoginStateGroup
from utils.sql import create_user, get_user_token, delete_user

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    try:
        await get_user_token(message.from_user.id)
        await state.set_state(LoginStateGroup.login)
        await state.set_data({})
        await message.answer('Выберите дальнейшие действия!', reply_markup=login_kb.get())
    except ValueError:
        await create_user(message.from_user.id)
        await message.answer(
            'Добрый день.\nЭтот бот поможет тебе проверить свои баллы. Для этого тебе достаточно войти в систему!',
            reply_markup=main_menu_kb.get())


@router.message(Text('Помощь'))
async def cmd_help(message: types.Message):
    await message.answer(text='Команда /start для начала работы\nПо любым вопросам @sickenedzick')


@router.message(LoginStateGroup.login, Text('Выйти'))
async def logout(message: types.Message, state: FSMContext):
    await state.clear()
    await delete_user(message.from_user.id)
    await message.answer('Вы успешно вышли из системы', reply_markup=types.ReplyKeyboardRemove)
    await message.answer('Выберите дальнейшие действия!', reply_markup=main_menu_kb.get())