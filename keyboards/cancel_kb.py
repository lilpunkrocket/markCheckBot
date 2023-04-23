from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get():
    kb = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Отменить')
        ]
    ], resize_keyboard=True, input_field_placeholder='Введите ваши данные')
    return kb
