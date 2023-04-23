from aiogram import Router, types, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from keyboards import cancel_kb, login_kb, main_menu_kb
from utils.assistants import get_token
from utils.sql import add_token
from states import LoginStateGroup


router = Router()


@router.message(Text('Войти'))
async def login(message: types.Message, state: FSMContext):
    await state.set_state(LoginStateGroup.username)
    await message.answer('Пожалуйста, введите Ваш логин!', reply_markup=cancel_kb.get())


@router.message(Text('Отменить'))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы отменили авторизацию.\n Можете в любой момент времени заново войти!')


@router.message(LoginStateGroup.username, F.text, lambda message: message.text.isnumeric() and len(message.text) == 10)
async def username_login(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(LoginStateGroup.password)
    await message.answer('Отлично😊\nТеперь пароль')


@router.message(LoginStateGroup.username)
async def username_login_error(message: types.Message):
    await message.reply('Пожалуйста, проверьте коррекность Ваших данных')


@router.message(LoginStateGroup.password, F.text, lambda message: message.text.isnumeric() and len(message.text) == 10)
async def password_login(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    try:
        token = await get_token(data['username'], data['password'])
        await add_token(message.from_user.id, token)
        await state.set_state(LoginStateGroup.login)
        await state.set_data({})
        await message.answer('Вы успешно зашли в систему🥳\nВыберите дальнейшие действия!', reply_markup=login_kb.get())
    except ValueError:
        await state.clear()
        await message.answer('Произошла какая-то ошибка🤕\nПожалуйста проверьте свои данные и попробуйте войти заново!',
                             reply_markup=main_menu_kb.get())


@router.message(LoginStateGroup.password)
async def password_login_error(message: types.Message):
    await message.reply('Пожалуйста, проверьте коррекность Ваших данных')
