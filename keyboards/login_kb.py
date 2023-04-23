from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get():
    kb = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Посмотреть свои баллы')
        ],
        [
            KeyboardButton(text='Профиль'),
            KeyboardButton(text='Выйти')
        ]
    ], resize_keyboard=True)
    return kb