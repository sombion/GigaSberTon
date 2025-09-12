from datetime import datetime
from fastapi import APIRouter, Depends, Query

from app.auth.dependency import get_current_user
from app.auth.models import Users
from app.signature.dao import SignatureDAO
from app.signature.schemas import SAddSignature
from app.signature.service import filter_signature, my_signature, search_signature

router = APIRouter(prefix="/signature", tags=["API signature"])


@router.get("/my")
async def my_signature_api(current_user: Users = Depends(get_current_user)):
    return await my_signature(current_user.id)


@router.post("/subscribe")
async def create_signature_api(
    signature_data: SAddSignature, current_user: Users = Depends(get_current_user)
):
    return await SignatureDAO.add(
        user_id=current_user.id, conclusion_id=signature_data.conclusion_id
    )


@router.get("/search/{text}")
async def search_signature_api(text: str):
    return await search_signature(text)


@router.get("/filter")
async def filter_signature_api(
    region: str | None = Query(None), departure_date: datetime | None = Query(None)
):
    return await filter_signature(region, departure_date)
