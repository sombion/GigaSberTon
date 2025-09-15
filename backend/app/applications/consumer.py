from loguru import logger
from pydantic import BaseModel
from app.applications.service import create_applications
from app.config import broker_router
from app.notification.service import make_notification


class ApplicationsData(BaseModel):
    tg_id: int
    data: dict


@broker_router.subscriber("applications")
async def process_order(application_data: ApplicationsData):
    tg_id = application_data.tg_id
    data = application_data.data
    await create_applications(
        tg_id,
        data.get("fio", ""),
        data.get("phone", ""),
        data.get("email", ""),
        data.get("cadastral_number", ""),
        data.get("problem", ""),
        data.get("address", ""),
    )
    # Сделать добавление в бд
    logger.debug(
        f"Заявление от: {tg_id}, успешно сохранено"
    )
