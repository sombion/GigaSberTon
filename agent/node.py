import json
import re
from loguru import logger

# from producer import send_application
from langchain.tools import tool
from state import State
from create_llm import llm
from langchain_core.messages import HumanMessage
from prompt import (
    info_agent_prompt,
    invalid_request_prompt,
    user_templates_prompt,
    not_fillled_data_user,
)


def filter_node(state: State):
    return {}


def check_user_data_node(state: State):
    return {}


def user_templates_node(state: State):
    user_text = state.get("input_messages", "")
    templates_data = state.get("templates_data", "")
    logger.debug(f"td: {templates_data}")
    messages = [
        {"role": "system", "content": user_templates_prompt},
        # {"role": "assistant", "content": templates_data},
        {
            "role": "user",
            "content": f"Сообщение от пользователя: {user_text}, текущие данные: {templates_data}",
        },
    ]
    # logger.debug(messages)
    response = llm.invoke(messages)
    answer = response.content.replace("`", "")
    # logger.debug(answer)

    # logger.debug(answer)
    return {"templates_data": answer}


def not_fillled_data_user_node(state: State):
    templates_data = state.get("templates_data", "")
    messages = [
        {"role": "system", "content": not_fillled_data_user},
        {"role": "assistant", "content": templates_data},
    ]
    responce = llm.invoke(messages)
    answer = responce.content
    return {"output_messages": answer, "templates_data": templates_data}


def check_data(templates_data: dict):
    fio = templates_data['fio']
    cadastral_number = templates_data['cadastral_number']
    address = templates_data['address']

    logger.debug(f"{fio} | {cadastral_number} | {address}")
    # Получение данных с рос

def safe_parse_agent_response(response: str) -> dict:
    try:
        # Ищем содержимое фигурных скобок
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if not match:
            raise ValueError("JSON не найден в ответе")
        return json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"Ошибка при парсинге ответа агента: {e}")


# Добавить проверку из реестра ... заявления
def humman_check_node(state: State):
    templates_data = state.get("templates_data")
    templates_data_dict = safe_parse_agent_response(templates_data)

    # Отправка данных на бэк
    # send_application()
    # Данные заполнены. Сообщаем пользователю о сохранении и сохраняем объединённые данные в templates_data
    logger.debug(templates_data_dict)
    check_data(templates_data_dict)
    return {"output_messages": "Заявление отправлено", "templates_data": templates_data}


def info_agent_node(state: State):
    user_text = state.get("input_messages", "")
    messages = [
        {"role": "system", "content": info_agent_prompt},
        {"role": "user", "content": f"Сообщение пользователя: {user_text}"},
    ]
    response = llm.invoke(messages)
    return {"output_messages": response.content}


def invalid_request_node(state: State):
    user_text = state.get("input_messages", "")
    messages = [
        {"role": "system", "content": invalid_request_prompt},
        {"role": "user", "content": f"Сообщение пользователя: {user_text}"},
    ]
    response = llm.invoke(messages)
    return {"output_messages": response.content}
