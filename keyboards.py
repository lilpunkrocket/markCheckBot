from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_menu_kb_template = [
    [
        types.KeyboardButton(text='/help'),
        types.KeyboardButton(text='/description'),
    ],
    [
        types.KeyboardButton(text='Random'),
    ]
]

kb_main_menu = types.ReplyKeyboardMarkup(keyboard=main_menu_kb_template, resize_keyboard=True)

kb_photo_descr = InlineKeyboardBuilder()

kb_photo_descr.row(
    types.InlineKeyboardButton(text='❤️', callback_data='like'),
    types.InlineKeyboardButton(text='👎', callback_data='dislike')
)

kb_photo_descr.row(
    types.InlineKeyboardButton(text='One more random image', callback_data='rand_img')
)

kb_photo_descr.row(
    types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
)
