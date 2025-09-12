from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.responses import FileResponse

from app.conclusion.dao import ConclusionDAO
from app.conclusion.service import (
    all_conclusions,
    download_conclusions,
    filter_conclusions,
    search_conclusions,
    view_conclusions,
)

router = APIRouter(prefix="/conclusion", tags=["API conclusion"])


# Создать create
@router.post("/create")
async def create_conclusions_api():
    return await ConclusionDAO.add()


# Создать edit
@router.patch("/update")
async def update_conclusions_api():
    return await ConclusionDAO.update()


@router.get("/all")
async def all_conclusions_api(id: int):
    return await all_conclusions()


@router.get("/detail/{id}")
async def detail_conclusions_api(id: int):
    return await ConclusionDAO.find_by_id(model_id=id)


@router.get("/search/{text}")
async def search_conclusions_api(text: str):
    return await search_conclusions(text)


@router.get("/filter")
async def filter_conclusions_api(
    region: str | None = Query(None), departure_date: datetime | None = Query(None)
):
    return await filter_conclusions(region, departure_date)


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
