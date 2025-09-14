from loguru import logger
from pydantic import BaseModel
from config import router


class TgData(BaseModel):
    tg_id: int
    text: str

class ApplicationData(BaseModel):
    tg_id: int
    data: dict


async def send_application(tg_id: int, data: dict):
    await router.broker.publish(
        {"tg_id": tg_id, "data": data},
        queue="applications",
        content_type="application/json",
    )
    logger.debug("applications ->")
    return 1


async def send_output_agent(agent_data: TgData):
    await router.broker.publish(
        agent_data.dict(),
        queue="output_agent",
        content_type="application/json",
    )
    logger.debug("output_agent ->")