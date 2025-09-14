from langchain_core.messages import HumanMessage
from fastapi import FastAPI
from config import router
from consumer import consumer_text

app = FastAPI()

app.include_router(router)

# from create_graph import graph
# from loguru import logger

# input_text = "У меня протекает крыша в доме, помоги составить мне заявление "

# responce = graph.invoke(
#     {"input_messages": input_text, "tg_id": 1},
#     config={"configurable": {"thread_id": 1}},
# )
# logger.info(responce["output_messages"])

# input_text = "Меня зовут Иванов Иван Иванович. Мой контактный телефон: +7 (900) 123-45-67, адрес электронной почты: ivanov.test@example.com. Кадастровый номер объекта недвижимости: 36:25:0301001:1234. Объект находится по адресу г. Воронеж, ул. Ленина, д. 15, кв. 10 . Координаты GPS местоположения проблемы: 51.6755, 39.2089."

# responce = graph.invoke(
#     {"input_messages": input_text, "tg_id": 1},
#     config={"configurable": {"thread_id": 1}},
# )
# logger.info(f"Ответ пользователю: {responce["output_messages"]}")
# logger.info(f"Данные: {responce["templates_data"]}")
