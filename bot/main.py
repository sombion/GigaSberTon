import asyncio
import logging
import sys

from aiogram import F, Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from pydantic import BaseModel

from config import settings

from faststream.rabbit import RabbitBroker


# --- Инициализация ---
dp = Dispatcher()
bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

broker = RabbitBroker(host=settings.RABBIT_HOST, port=settings.RABBIT_PORT)


# --- Модель данных для Rabbit ---
class TgData(BaseModel):
    tg_id: int
    text: str


# --- Подписчики брокера ---
@broker.subscriber("notification")
async def notification_user(data: TgData):
    await bot.send_message(chat_id=data.tg_id, text=data.text)
    logging.info("-> notification")


@broker.subscriber("output_agent")
async def output_agent_messages(data: TgData):
    await bot.send_message(chat_id=data.tg_id, text=data.text)
    logging.info("-> output_agent")


# --- /start ---
@dp.message(CommandStart())
async def handle_start(msg: Message):
    logging.info(f"User {msg.chat.id} started bot")
    await msg.answer(
        "👋 Добро пожаловать в <b>AI-агента ЖКХ</b>!\n\n"
        "Я помогу вам подготовить заявление о пригодности жилья.\n\n"
        "Для списка команд введите /help"
    )


# --- /help ---
@dp.message(Command("help"))
async def handle_help(msg: Message):
    await msg.answer(
        "📌 <b>Доступные команды</b>:\n\n"
        "/start – начать работу\n"
        "/help – список команд\n"
        "/info – информация о боте\n"
        "/support – контакты поддержки\n"
        "/all – список всех поданных заявлений\n"
        "/end – список завершённых заявлений\n"
        "/current id – информация по заявлению\n"
        "/delete id – удаление заявления (если статус 'новое')"
    )


# --- /info ---
@dp.message(Command("info"))
async def handle_info(msg: Message):
    await msg.answer(
        "ℹ️ <b>Общая информация</b>\n\n"
        "Этот бот помогает жителям подготовить заявления "
        "на оценку пригодности жилых помещений.\n\n"
        "⚙️ Как это работает:\n"
        "1. Вы вводите данные (ФИО, адрес, контакты).\n"
        "2. AI-агент формирует заявление по шаблону.\n"
        "3. Готовый документ отправляется вам сюда."
    )


# --- /support ---
@dp.message(Command("support"))
async def handle_support(msg: Message):
    await msg.answer(
        "📞 <b>Контакты поддержки</b>\n\n"
        "✉️ Email: support@example.com\n"
        "☎️ Телефон: +7 (999) 123-45-67"
    )


# --- /all ---
@dp.message(Command("all"))
async def handle_all(msg: Message):
    # 🔹 Здесь будет запрос к Rabbit / БД
    await msg.answer(
        "📑 <b>Ваши поданные заявления</b>:\n\n"
        "1. Заявление по адресу: ул. Ленина, 10 (статус: новое)\n"
        "2. Заявление по адресу: пр. Мира, 25 (статус: в работе)\n"
        "3. Заявление по адресу: ул. Горького, 5 (статус: завершено)"
    )


# --- /end ---
@dp.message(Command("end"))
async def handle_end(msg: Message):
    # 🔹 Здесь будет запрос к Rabbit / БД
    await msg.answer(
        "✅ <b>Завершённые заявления</b>:\n\n"
        "3. Заявление по адресу: ул. Горького, 5 (Заключение: помещение непригодно)"
    )


# --- /current <id> ---
@dp.message(Command("current"))
async def handle_current(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await msg.answer("⚠️ Укажите ID заявления. Пример: /current 3")
        return

    app_id = int(parts[1])
    # 🔹 Здесь будет запрос к Rabbit / БД
    await msg.answer(
        f"📌 <b>Заявление #{app_id}</b>\n\n"
        "👤 ФИО: Иванов Иван Иванович\n"
        "🏠 Адрес: ул. Горького, 5\n"
        "📞 Телефон: +7 999 123-45-67\n"
        "📧 Email: ivan@example.com\n\n"
        "📋 Статус: завершено\n"
        "📑 Заключение комиссии: помещение непригодно"
    )


# --- /delete <id> ---
@dp.message(Command("delete"))
async def handle_delete(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await msg.answer("⚠️ Укажите ID заявления. Пример: /delete 4")
        return

    app_id = int(parts[1])
    # 🔹 Здесь будет проверка статуса через Rabbit / БД
    status = "новое"  # пример

    if status != "новое":
        await msg.answer(f"❌ Заявление №{app_id} нельзя удалить (статус: {status})")
    else:
        await msg.answer(f"🗑 Заявление №{app_id} успешно удалено")


@dp.message(F.text)
async def send_agent(message: Message):
    tg_id = message.chat.id
    text = message.text
    logging.info(f"Получено от пользователя: {text} ({tg_id})")

    # Отправляем в Rabbit
    await broker.publish(
        {"tg_id": tg_id, "text": text},
        queue="input_agent",
        content_type="application/json",
    )
    logging.info("input_agent ->")
    # await message.answer("✅ Ваши данные отправлены AI-агенту, ожидайте ответ...")


# --- Запуск ---
async def main() -> None:
    async with broker:
        logging.info("Брокер стартовал")
        await broker.start()
        await dp.start_polling(bot)
    logging.info("Все закончилось...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
