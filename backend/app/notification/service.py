from app.config import broker_router
from app.notification.dao import NotificationDAO
from app.notification.models import Notification


async def make_notification(tg_id: int, text: str):
    await broker_router.broker.publish(
        {"tg_id": tg_id, "text": text},
        queue="notification",
        content_type="application/json",
    )
    return {"data": "OK"}

async def all_notification(user_id: int):
    notification_data: Notification = await NotificationDAO.find_all(user_id=user_id)
    notification_count: str = await NotificationDAO.my_count(user_id=user_id)
    return {
        "count": notification_count,
        "notifications": notification_data
    }