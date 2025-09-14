from sqladmin import ModelView
from app.applications.models import Applications
from app.auth.models import Users


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
