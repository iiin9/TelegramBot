import datetime
import re
from loguru import logger
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config
import sel_2

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")
bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
regular = "[А, В, Е, К, М, Н, О, Р, С, Т, У, Х][0-9]{3}[А, В, Е, К, М, Н, О, Р, С, Т, У, Х]{2}[0-9]{2,3}"
regular2 = '^([Бб]{1}[Оо]{1}[Тт]{1}) ([0-2]{0,1}[0-9]{1}):([0-6]{0,1}[0-9]{1}) ([0-9{0,3}]) ([0-9]{0,3})'


@dp.message_handler(commands="start")
async def cmd_start(msg: types.Message):
    logger.info(f"{msg.from_user}, {msg.text}")
    await msg.answer("Введите гос.номер формата А123АА123")


@logger.catch()
@dp.message_handler(
    lambda message: re.fullmatch(
        regular,
        str(message.text).upper(),
    )
)
async def without_pure(msg: types.Message):
    logger.info(f"{msg.from_user}, {msg.text}")
    msg_0 = await msg.answer("Номер распознан.")
    data_dict = sel_2.search(msg.text)
    msg_data = f"<code><b>{data_dict['Госномер']}</b></code>\n{data_dict['Марка']}, {data_dict['Модель']}, {data_dict['Год выпуска']} года, {data_dict['Мощность, л.с.']} л.с.\nVIN: <code>{data_dict['Номер VIN']}</code>\nСТС: <code>{data_dict['Серия и номер СТС']}</code>\nДата выдачи СТС: {data_dict['Дата выдачи СТС']}"
    logger.info(f"ANSWER:{msg.chat.id}, {data_dict}")
    await msg.answer(text=msg_data, parse_mode=types.ParseMode.HTML)
    await bot.delete_message(msg_0.chat.id, msg_0.message_id)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(call: types.CallbackQuery):
    logger.info(f"{call.from_user}, {call.data}")
    code = call.data
    if code == "all":
        await call.message.answer("Скоро будет")
        # await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@dp.message_handler(
    lambda message: re.fullmatch(regular2, str(message.text).upper()))
async def olyabot(msg: types.Message):
    logger.info(f"{msg.from_user}, {msg.text}")
    message = msg.text.split()
    time_start = message[1]
    time_work = message[2]
    iterations = message[3]
    await msg.answer(f'Команда распознана, время запуска: {time_start}, время работы: {time_work}, итераций:{iterations}')


@dp.message_handler()
async def echo_message(msg: types.Message):
    logger.info(f"{msg.from_user}, {msg.text}")
    await bot.send_message(msg.from_user.id, msg.text, parse_mode=types.ParseMode.HTML)


if __name__ == "__main__":
    executor.start_polling(dp)
