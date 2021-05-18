import re

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config
import sel_2

bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Введите гос.номер формата А123АА123")


@dp.message_handler(
    lambda message: re.fullmatch(
        r"[А, В, Е, К, М, Н, О, Р, С, Т, У, Х]\d\d\d[А, В, Е, К, М, Н, О, Р, С, Т, У, Х]{2}\d{2,3}",
        str(message.text).upper(),
    )
)
async def without_pure(msg: types.Message):
    msg_0 = await msg.answer("Номер распознан.")
    msg_data = sel_2.search(msg.text)
    await msg.answer(text=msg_data, parse_mode=types.ParseMode.HTML)
    await bot.delete_message(msg_0.chat.id, msg_0.message_id)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(call: types.CallbackQuery):
    code = call.data
    if code == "all":
        await call.message.answer("toDo")
        # await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text, parse_mode=types.ParseMode.HTML)


if __name__ == "__main__":
    executor.start_polling(dp)
