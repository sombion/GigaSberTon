import asyncio
import logging
import sys
from aiogram import F

from pydantic import BaseModel
from config import settings

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from faststream.rabbit import RabbitBroker

dp = Dispatcher()
bot = Bot(token=settings.BOT_TOKEN)

broker = RabbitBroker()


class TgData(BaseModel):
    tg_id: int
    text: str


@broker.subscriber("notification")
async def notification_user(data: TgData):
    await bot.send_message(
        chat_id=data.tg_id,
        text=data.text,
    )
    logging.info("-> notification")


@broker.subscriber("output_agent")
async def output_agent_messages(data: TgData):
    await bot.send_message(
        chat_id=data.tg_id,
        text=data.text,
    )
    logging.info("-> output_agent")


@dp.message(CommandStart())
async def handle_msg(msg: Message):
    logging.info(msg.chat.id)
    await msg.answer(f"Добро пожаловать в AI агента ЖКХ, готов помочь в создании заявления")


@dp.message(F.text)
async def send_agent(message: Message):
    tg_id = message.chat.id
    text = message.text
    logging.info(text)
    logging.info(tg_id)
    # Отправляем в Rabbit
    await broker.publish(
        {"tg_id": tg_id, "text": text},
        queue="input_agent",
        content_type="application/json",
    )
    logging.info("input_agent ->")


async def main() -> None:
    async with broker:
        await broker.start()
        logging.info("Брокер стартовал")
        await dp.start_polling(bot)
    logging.info("Все закончилось...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
