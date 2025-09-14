from datetime import datetime
from fastapi import APIRouter, Depends, Query

from app.auth.dependency import get_current_user
from app.auth.models import Users
from app.signature.schemas import SAddSignature
from app.signature.service import (
    filter_signature,
    all,
    search_signature,
    update_signature,
)

router = APIRouter(prefix="/api/signature", tags=["API signature"])


@router.get("/all")
async def all_signature_api(current_user: Users = Depends(get_current_user)):
    return await all()


@router.post("/subscribe")
async def create_signature_api(
    signature_data: SAddSignature, current_user: Users = Depends(get_current_user)
):
    return await update_signature(
        users_id=current_user.id, conclusion_id=signature_data.conclusion_id
    )


@router.get("/search/{text}")
async def search_signature_api(text: str):
    return await search_signature(text)


@router.get("/filter")
async def filter_signature_api(
    street: str | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
):
    return await filter_signature(street, date_from, date_to)
