import json
import re
from loguru import logger

# from producer import send_application
from producer import send_application
from state import State
from create_llm import llm
from langchain_core.messages import HumanMessage
from prompt import (
    info_agent_prompt,
    invalid_request_prompt,
    user_templates_prompt,
    not_fillled_data_user_prompt,
    confirmation_final_prompt,
)


async def filter_node(state: State):
    return {}


async def check_user_data_node(state: State):
    return {}


async def confirmation_node(state: State):
    return {}


async def change_node(state: State):
    logger.debug("change_node")
    return {"output_messages": "Напишите что хотите изменить", "await_response": None}


async def user_templates_node(state: State):
    logger.debug("user_templates_node")
    user_text = state.get("input_messages", "")
    templates_data = state.get("templates_data", "")
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


async def not_fillled_data_user_node(state: State):
    logger.debug("not_fillled_data_user_node")
    templates_data = state.get("templates_data", "")
    messages = [
        {"role": "system", "content": not_fillled_data_user_prompt},
        {"role": "assistant", "content": templates_data},
    ]
    responce = llm.invoke(messages)
    answer = responce.content
    return {"output_messages": answer, "templates_data": templates_data}


def check_data(templates_data: dict):
    fio = templates_data["fio"]
    cadastral_number = templates_data["cadastral_number"]
    address = templates_data["address"]

    logger.debug(f"Проверка данных с егрн: {fio} | {cadastral_number} | {address}")


def safe_parse_agent_response(response: str) -> dict:
    try:
        # Ищем содержимое фигурных скобок
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if not match:
            raise ValueError("JSON не найден в ответе")
        return json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"Ошибка при парсинге ответа агента: {e}")


async def humman_check_node(state: State):
    logger.debug("humman_check_node")
    templates_data = state.get("templates_data")
    templates_data_dict = safe_parse_agent_response(templates_data)

    logger.debug(templates_data_dict)
    check_data(templates_data_dict)
    return {"templates_data": templates_data}


async def confirmation_final_node(state: State):
    logger.debug("confirmation_node")
    await_response = state.get("await_response", "")
    templates_data = state.get("templates_data")
    if not await_response:
        messages = [
            {"role": "system", "content": confirmation_final_prompt},
            {"role": "assistant", "content": templates_data},
        ]
        responce = llm.invoke(messages)
        answer = responce.content
        return {"output_messages": answer, "await_response": True}


async def info_agent_node(state: State):
    logger.debug("info_agent_node")
    user_text = state.get("input_messages", "")
    messages = [
        {"role": "system", "content": info_agent_prompt},
        {"role": "user", "content": f"Сообщение пользователя: {user_text}"},
    ]
    response = llm.invoke(messages)
    return {"output_messages": response.content}


async def invalid_request_node(state: State):
    logger.debug("invalid_request_node")
    user_text = state.get("input_messages", "")
    messages = [
        {"role": "system", "content": invalid_request_prompt},
        {"role": "user", "content": f"Сообщение пользователя: {user_text}"},
    ]
    response = llm.invoke(messages)
    return {"output_messages": response.content}

async def send_applications_node(state: State):
    tg_id = state.get("tg_id")
    templates_data = state.get("templates_data")
    templates_data = safe_parse_agent_response(templates_data)
    logger.debug("send_applications_node")

async def send_applications_node(state: State):
    tg_id = state.get("tg_id")
    templates_data = state.get("templates_data")
    templates_data = safe_parse_agent_response(templates_data)
    logger.debug("send_applications_node")

    await send_application(tg_id, templates_data)

    return {"output_messages": "Заявление отправлено", "await_response": None}
