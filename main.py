import asyncio
import logging

import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text

from config import settings
from utils import HELP_TEXT
from keyboards import kb_main_menu, kb_photo_descr

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.bot_token.get_secret_value())
bot.get_updates(offset=-1)
dp = Dispatcher()


async def send_random(message: types.Message):
    img = requests.request(method='GET', url='https://picsum.photos/1024')
    await bot.send_photo(message.chat.id, photo=img.url, reply_markup=kb_photo_descr.as_markup())


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer('Бот успешно запущен', reply_markup=kb_main_menu)


@dp.callback_query(Text('main_menu'))
async def cmd_start(callback: types.CallbackQuery):
    await callback.message.answer('Что дальше?', reply_markup=kb_main_menu)
    await callback.message.delete()
    await callback.answer()


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await bot.send_message(message.from_user.id, HELP_TEXT, reply_markup=types.ReplyKeyboardRemove)


@dp.message(Text('Random'))
async def cmd_random_photo(message: types.Message):
    msg = await message.answer(text='Here is your random photo', reply_markup=types.ReplyKeyboardRemove)
    await msg.delete()
    await send_random(message)


@dp.callback_query(Text('rand_img'))
async def callback_random_img(callback: types.CallbackQuery):
    img = requests.request(method='GET', url='https://picsum.photos/1024')
    await callback.message.edit_media(types.InputMedia(media=img.url, type='photo'),
                                      reply_markup=kb_photo_descr.as_markup())
    await callback.answer()


flag = False


@dp.callback_query(Text('like'))
async def callback_like(callback: types.CallbackQuery):
    global flag
    if not flag:
        await callback.answer('Вам понравилось', show_alert=True)
        flag = not flag
    else:
        await callback.answer('Вы уже ставили лайк', show_alert=True)


@dp.callback_query(Text('dislike'))
async def callback_dislike(callback: types.CallbackQuery):
    await callback.answer('Вам не понравилось', show_alert=True)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
