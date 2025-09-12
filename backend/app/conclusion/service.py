from datetime import datetime
import mimetypes
import os
from fastapi.responses import FileResponse
from app.conclusion.dao import ConclusionDAO


async def create_conclusions():
    ...

async def edit_conclusions():
    ...

async def all_conclusions():
    conclusion_data = await ConclusionDAO.find_all()
    return {"count": len(conclusion_data), "applications": conclusion_data}


async def search_conclusions(text: str):
    try:
        text = int(text)
    except Exception as e:
        print(e)
    conclusion_data = await ConclusionDAO.search(text)
    return {"count": len(conclusion_data), "conclusions": conclusion_data}

async def filter_conclusions(
    region: str | None, departure_date: datetime
):
    conclusion_data = await ConclusionDAO.filter(
        region, departure_date
    )
    return {"count": len(conclusion_data), "conclusions": conclusion_data}


async def view_conclusions():
    conclusion_data = await ConclusionDAO.find_by_id(id)
    if not conclusion_data:
        return {"detail": "Файл не найден"}
    file_path = conclusion_data.file_url
    ext = os.path.splitext(file_path)[1].lower()
    media_type, _ = mimetypes.guess_type(file_path)
    if not media_type:
        media_type = "application/octet-stream"
    return FileResponse(path=file_path, media_type=media_type)


async def download_conclusions():
    conclusion_data = await ConclusionDAO.find_by_id(id)
    if not conclusion_data:
        return {"detail": "Файл не найден"}
    return conclusion_data.file_url
