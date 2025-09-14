from loguru import logger
from state import State
from create_llm import llm
from prompt import filter_prompt
from prompt import check_user_data_prompt, confirmation_prompt, change_prompt


async def filter_router(state: State):
    user_text = state.get("input_messages", "")
    output_messages = state.get("output_messages", "")
    await_response = state.get("await_response", "")

    if await_response:
        return "confirmation_node"

    messages = [
        {"role": "system", "content": filter_prompt},
        {"role": "assistant", "content": output_messages},
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


async def check_user_data_router(state: State):
    templates_data = state.get("templates_data", "null")
    messages = [
        {"role": "system", "content": check_user_data_prompt},
        {"role": "assistant", "content": templates_data},
    ]

    responce = llm.invoke(messages)
    answer = responce.content

    logger.debug(f"check_user_data_router: {answer}")

    if "True" in answer:
        return "True"
    return "False"


async def confirmation_router(state: State):
    await_response = state.get("await_response")
    if not await_response:
        return "confirmation_final_node"
    if await_response:
        messages = [
            {
                "role": "system",
                "content": confirmation_prompt,
            },
            {"role": "user", "content": state.get("input_messages")},
        ]
        responce = llm.invoke(messages)
        answer = responce.content
        logger.debug(f"answer: {answer}")
        if "Да" in answer:
            return "send_applications_node"
        else:
            return "change_node"


async def change_router(state: State):
    input_messages = state.get("input_messages")
    messages = [
        {"role": "system", "content": change_prompt},
        {"role": "user", "content": input_messages}
    ]
    responce = llm.invoke(messages)
    answer = responce.content

    if "Да" in answer:
        return "filter_node"

    return "END"
