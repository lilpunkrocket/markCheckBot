import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from utils.config import settings
from utils.sql import initialize_db, close_db
from handlers import base, auth, profile, marks

logging.basicConfig(level=logging.INFO)


async def main():
    # bot = Bot(settings.bot_token.get_secret_value())  # create our bot
    bot = Bot(os.getenv('BOT_TOKEN'))
    await bot.get_updates(offset=-1)  # skip updates
    dp = Dispatcher()  # create our dispatcher

    dp.include_routers(base.router, auth.router, profile.router, marks.router)

    dp.startup.register(initialize_db)  # register our database on bots startup
    dp.shutdown.register(close_db)  # close connection with database on bots shutdown
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
