import mimetypes
import os
from datetime import datetime
from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.applications.dao import ApplicationsDAO
from app.applications.models import ApplicationStatus, Applications
from app.notification.service import make_notification


async def create_applications(
    file: UploadFile,
    tg_id: int,
    tg_username: str,
    fio: str,
    phone: str,
    email: str,
    cadastral_number: str,
    region: str,
    gps_lat: float,
    gps_lng: float,
):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_ext = os.path.splitext(file.filename)[1] or ""
    safe_filename = f"{timestamp}{file_ext}"
    upload_dir = "doc/application"
    os.makedirs(upload_dir, exist_ok=True)  # создаём директорию если её нет

    file_path = os.path.join(upload_dir, safe_filename)

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    application = await ApplicationsDAO.add(
        tg_id=tg_id,
        fio=fio,
        phone=phone,
        email=email,
        cadastral_number=cadastral_number,
        region=region,
        gps_lat=gps_lat,
        gps_lng=gps_lng,
        file_url=file_path,
    )

    return {"detail": "Заявление успешно создано", "application": application}


async def delete_applications(id: int):
    application_data = await ApplicationsDAO.find_by_id(id)
    if not application_data:
        raise {"detail": "Заявка не найдена"}
    if application_data.status != ApplicationStatus.ACCEPTED:
        raise {"detail": "Невозможно удалить заявление"}
    application_data = await ApplicationsDAO.delete(id)
    os.remove(application_data.file_url)
    return {"detail": "Заявление успешно удалено", "application": application_data}


async def all_applications():
    application_data = await ApplicationsDAO.find_all()
    return {"count": len(application_data), "applications": application_data}


async def download_applications(id: int):
    application_data = await ApplicationsDAO.find_by_id(id)
    if not application_data:
        return {"detail": "Файл не найден"}
    return application_data.file_url


async def view_applications(id: int):
    application_data = await ApplicationsDAO.find_by_id(id)
    if not application_data:
        return {"detail": "Файл не найден"}
    file_path = application_data.file_url
    ext = os.path.splitext(file_path)[1].lower()
    media_type, _ = mimetypes.guess_type(file_path)
    if not media_type:
        media_type = "application/octet-stream"
    return FileResponse(path=file_path, media_type=media_type)


async def search_applications(text: str):
    try:
        text = int(text)
    except Exception as e:
        print(e)
    applications_data = await ApplicationsDAO.search(text)
    return {"count": len(applications_data), "applications": applications_data}


async def filter_applications(
    region: str | None, departure_date: datetime, is_departure: bool
):
    applications_data = await ApplicationsDAO.filter(
        region, departure_date, is_departure
    )
    return {"count": len(applications_data), "applications": applications_data}

async def update_departure(applications_id: int, departure_date: datetime):
    application_data: Applications = ApplicationsDAO.find_by_id(applications_id)
    if not application_data:
        raise {"detail": "заявка не найдена"}
    if application_data.departure_date:
        raise {"detail": "Дата выезда уже назначена"}

    application_data = await ApplicationsDAO.departure(applications_id, departure_date)
    await make_notification(application_data.tg_id, f"Для заявки {applications_id} назначен выезд на {departure_date}")
    return {
        "detail": "Выезд успешно назначен"
    }