from loguru import logger
from pydantic import BaseModel
from config import router


class TgData(BaseModel):
    tg_id: int
    text: str

class ApplicationData(BaseModel):
    tg_id: int
    data: dict


async def send_application(application_data: TgData):
    await router.broker.publish(
        application_data.dict(),
        queue="application",
        content_type="application/json",
    )
    logger.debug("application ->")


async def send_output_agent(agent_data: TgData):
    await router.broker.publish(
        agent_data.dict(),
        queue="output_agent",
        content_type="application/json",
    )
    logger.debug("output_agent ->")
