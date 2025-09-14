from loguru import logger
from pydantic import BaseModel
from app.config import broker_router


class ApplicationsData(BaseModel):
    tg_id: int
    text: dict


@broker_router.subscriber("applications")
async def process_order(application_data: ApplicationsData):
    # Сделать добавление в бд
    logger.debug(
        f"Пользователь: {application_data.tg_id}\nТекст: {application_data.text}"
    )
