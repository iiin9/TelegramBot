import os
import re

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import sel_2

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Введите гос.номер формата А123АА123")


@dp.message_handler(lambda message: re.fullmatch(
    r"[А, В, Е, К, М, Н, О, Р, С, Т, У, Х]\d\d\d[А, В, Е, К, М, Н, О, Р, С, Т, У, Х]{2}\d{2,3}", str(message.text).upper()))
async def without_pure(message: types.Message):
    await message.answer("Номер распознан.")
    ans = sel_2.search(message.text)
    if 'Не указан параметр' in ans:
        await message.reply("Возникла ошибка при проверке.")
    else:
        await message.answer(ans, parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text, parse_mode=types.ParseMode.HTML)


if __name__ == "__main__":
    executor.start_polling(dp)
