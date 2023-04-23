from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get():
    kb = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Войти')
        ],
        [
            KeyboardButton(text='Помощь')
        ]
    ], resize_keyboard=True, input_field_placeholder='Войдите в свой аккаунт')
    return kb