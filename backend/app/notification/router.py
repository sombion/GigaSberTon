from fastapi import APIRouter, Depends

from app.auth.dependency import get_current_user
from app.auth.models import Users
from app.notification.dao import NotificationDAO
from app.notification.schemas import SNotificationId, SNotificationAll
from app.notification.service import make_notification


router = APIRouter(prefix="/api/notification", tags=["API для работы с уведомлениями"])


@router.post("/send-test")
async def make_notification_api(tg_id: int, text: str):
    return await make_notification(tg_id, text)


@router.get("/my")
async def my_notification_api(current_user: Users = Depends(get_current_user)):
    notifications_data = await NotificationDAO.find_all(
        user_id=current_user.id, read=False
    )
    return {"count": len(notifications_data), "notifications": notifications_data}


@router.get("/all")
async def all_notification_api(current_user: Users = Depends(get_current_user)):
    notifications_data = await NotificationDAO.find_all(user_id=current_user.id)
    return {"count": len(notifications_data), "notifications": notifications_data}


@router.post("/read")
async def read_notification_api(notification_data: SNotificationId):
    await NotificationDAO.update(notification_data.id)
    return {"detail": "Уведомление успешно прочитано"}


@router.post("/read-all")
async def read_all_notification_api(notification_data: SNotificationAll):
    [await NotificationDAO.update(id) for id in notification_data.id_list]
    return {"detail": "Уведомления успешно прочитаны"}


@router.delete("/delete")
async def delete_notification_api(notification_data: SNotificationId):
    await NotificationDAO.delete(id=notification_data.id)
    return {"detail": "Уведомление успешно удалено"}
