import logging
from aiogram import types
from aiogram import Bot, Dispatcher
from core.handlers.basic import get_start
import asyncio
from core.settings import settings
from aiogram.filters import Command

TOKEN = '6978695252:AAEqDImOYxp0bVZo34gwlytI9IG7Bpn1GP4'
bot = Bot(TOKEN)


async def start_bot(bot:Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот запущен!")


async def stop_bot(bot:Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот остановлен!")


async def on_chat_member_join(message: types.Message):
    user = message.new_chat_members[0]
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"Добро пожаловать, {user.first_name}! Надеемся, вам здесь понравится.")


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    dp = Dispatcher(bot=settings.bots.bot_token, parse_mode='HTML')

    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.message.register(on_chat_member_join)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())