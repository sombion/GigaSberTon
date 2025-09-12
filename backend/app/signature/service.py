from datetime import datetime
from app.signature.dao import SignatureDAO


async def my_signature(users_id: int):
    signature_data = await SignatureDAO.find_all(users_id=users_id)
    return {"count": len(signature_data), "signatures": signature_data}

async def search_signature(text: str):
    try:
        text = int(text)
    except Exception as e:
        print(e)
    signatures_data = await SignatureDAO.search(text)
    return {"count": len(signatures_data), "applications": signatures_data}


async def filter_signature(
    region: str | None, departure_date: datetime
):
    signatures_data = await SignatureDAO.filter(
        region, departure_date
    )
    return {"count": len(signatures_data), "applications": signatures_data}
