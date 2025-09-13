from datetime import datetime
from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse

from app.auth.dependency import get_current_user
from app.auth.models import Users
from app.conclusion.dao import ConclusionDAO
from app.conclusion.schemas import SCreateConclusion
from app.conclusion.service import (
    all_conclusions,
    create_conclusions,
    download_conclusions,
    filter_conclusions,
    search_conclusions,
    view_conclusions,
)

router = APIRouter(prefix="/api/conclusion", tags=["API conclusion"])


@router.post("/create")
async def create_conclusions_api(conclusion_data: SCreateConclusion):
    return await create_conclusions(
        conclusion_data.applications_id,
        conclusion_data.date,
        conclusion_data.chairman_id,
        conclusion_data.members_id,
        conclusion_data.justification,
        conclusion_data.documents,
        conclusion_data.conclusion,
    )


# Создать edit
@router.patch("/update")
async def update_conclusions_api():
    return await ConclusionDAO.update()


@router.get("/all")
async def all_conclusions_api():
    return await all_conclusions()


@router.get("/detail/{id}")
async def detail_conclusions_api(id: int):
    return await ConclusionDAO.find_by_id(model_id=id)


@router.get("/search/{text}")
async def search_conclusions_api(text: str):
    return await search_conclusions(text)


@router.get("/filter")
async def filter_conclusions_api(
    street: str | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    signed: bool | None = Query(None),
    current_user: Users = Depends(get_current_user)
):
    return await filter_conclusions(street, date_from, date_to, signed, current_user.id)


@router.get("/download/{id}")
async def download_conclusions_api(id: int):
    file_path = await download_conclusions(id)
    return FileResponse(
        path=file_path,
        filename=str(id),
        media_type="application/octet-stream",
    )


@router.get("/view/{id}")
async def view_conclusions_api(id: int):
    return await view_conclusions(id)
