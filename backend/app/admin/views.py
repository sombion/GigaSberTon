from sqladmin import ModelView
from app.applications.models import Applications
from app.auth.models import Users
from app.conclusion.models import Conclusion
from app.notification.models import Notification
from app.signature.models import Signature


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.login, Users.fio, Users.email]
    column_details_exclude_list = [Users.hash_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class ApplicationsAdmin(ModelView, model=Applications):
    column_list = [
        Applications.id,
        Applications.tg_id,
        Applications.fio,
        Applications.phone,
        Applications.email,
        Applications.cadastral_number,
        Applications.address,
        Applications.street,
        Applications.file_url,
        Applications.status,
        Applications.departure_date,
    ]
    name = "Заявка"
    name_plural = "Заявки"

class ConclusionAdmin(ModelView, model=Conclusion):
    column_list = [
        Conclusion.id,
        Conclusion.applications_id,
        Conclusion.create_date,
        Conclusion.file_url,
    ]
    name = "Заявление"
    name_plural = "Заявления"

class SignatureAdmin(ModelView, model=Signature):
    column_list = [
        Signature.id,
        Signature.users_id,
        Signature.conclusion_id,
        Signature.signed,
    ]
    name = "Подпись"
    name_plural = "Подписи"

class NotificationAdmin(ModelView, model=Notification):
    column_list = [
        Notification.id,
        Notification.user_id,
        Notification.text,
        Notification.created_at,
        Notification.read,
    ]
    name = "Уведомление"
    name_plural = "Уведомления"