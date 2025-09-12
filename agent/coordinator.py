from loguru import logger
from state import State
from create_llm import llm
from prompt import filter_prompt
from langchain_core.messages import HumanMessage, SystemMessage


def filter_router(state: State):
    user_text = state.get("input_messages", "")
    messages = [
        {"role": "system", "content": filter_prompt},
        {"role": "user", "content": f"Сообщение пользователя: {user_text}"},
    ]

    responce = llm.invoke(messages)
    answer = responce.content

    logger.debug(f"filter_router: {answer}")

    if "user_templates_node" in answer:
        return "user_templates_node"

    if "info_agent_node" in answer:
        return "info_agent_node"

    return "invalid_request_node"


def check_user_data_router(state: State):
    templates_data = state.get("templates_data", "null")
    system_prompt = "Твоя задача проверь заполнил ли пользователь все данные, если пользователь заполнил не все данные напиши 'False', если пользователь заполнил весь шаблон, напиши 'True'. В ответе пиши только 'True' или 'False'"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": templates_data}
    ]

    responce = llm.invoke(messages)
    answer = responce.content
    
    logger.debug(f"check_user_data_router: {answer}")

    if "True" in answer:
        return "True"
    return "False"