from fastapi import APIRouter, Depends

from app.auth.dependency import get_current_user
from app.auth.models import Users
from app.notification.dao import NotificationDAO
from app.notification.schemas import SNotificationId, SNotificationAll
from app.notification.service import all_notification, make_notification


router = APIRouter(prefix="/api/notification", tags=["API для работы с уведомлениями"])


@router.post("/make")
async def make_notification_api(tg_id: int, text: str):
    return await make_notification(tg_id, text)

@router.post("/add")
async def add_notification_api(user_id: int, text: str):
    return await NotificationDAO.add(user_id, text)

@router.get("/all")
async def all_notification_api(current_user: Users = Depends(get_current_user)):
    return await all_notification(current_user.id)


@router.post("/read")
async def read_notification_api(notification_data: SNotificationId):
    await NotificationDAO.update(notification_data.id)
    return {"detail": "Уведомление успешно прочитано"}


@router.get("/read-all")
async def read_all_notification_api(current_user: Users = Depends(get_current_user)):
    await NotificationDAO.read_all(current_user.id)
    return {"detail": "Уведомления успешно прочитаны"}


@router.delete("/delete")
async def delete_notification_api(notification_data: SNotificationId):
    await NotificationDAO.delete(id=notification_data.id)
    return {"detail": "Уведомление успешно удалено"}
