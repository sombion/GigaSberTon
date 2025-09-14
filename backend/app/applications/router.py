from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import FileResponse

from app.applications.dao import ApplicationsDAO
from app.applications.models import ApplicationStatus
from app.applications.schemas import SApplicationsDeparture, SCreateApplications
from app.applications.service import (
    all_applications,
    create_applications,
    delete_applications,
    download_applications,
    filter_applications,
    search_applications,
    update_departure,
    view_applications,
)
from app.auth.dependency import get_current_user
from app.auth.models import Users

router = APIRouter(prefix="/api/applications", tags=["API applications"])


@router.post("/create")
async def create_applications_api(applications_data: SCreateApplications):
    return await create_applications(
        applications_data.tg_id,
        applications_data.fio,
        applications_data.phone,
        applications_data.email,
        applications_data.cadastral_number,
        applications_data.address,
    )

# Проверить (реализовать уведомления, изменение даты и статуса)
# Для какого-то заявления уже есть выезд

@router.patch("/departure")
async def update_departure_api(
    application_data: SApplicationsDeparture,
    current_user: Users = Depends(get_current_user),
):
    return await update_departure(
        application_data.applications_id, application_data.departure_date
    )

@router.delete("/delete/{id}")
async def delete_applications_api(id: int):
    return await delete_applications(id)


@router.get("/all")
async def all_applications_api():
    return await all_applications()


@router.get("/detail/{id}")
async def detail_applications_api(id: int):
    return await ApplicationsDAO.find_by_id(model_id=id)


@router.get("/search/{text}")
async def search_applications_api(text: str):
    return await search_applications(text)


@router.get("/filter")
async def filter_applications_api(
    street: str | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    is_departure: bool | None = Query(None),
):
    return await filter_applications(street, date_from, date_to, is_departure)


@router.get("/street")
async def addres_api(search: str | None = Query(None)):
    return {"streets": await ApplicationsDAO.get_street(search)}


@router.get("/download/{id}")
async def download_application_api(id: int):
    file_path = await download_applications(id)
    return FileResponse(
        path=file_path,
        filename=str(id),
        media_type="application/octet-stream",
    )


@router.get("/view/{id}")
async def view_application_api(id: int):
    return await view_applications(id)