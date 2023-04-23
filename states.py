# Here will be placed our states
from aiogram.fsm.state import StatesGroup, State


class LoginStateGroup(StatesGroup):
    username = State()
    password = State()
    login = State()