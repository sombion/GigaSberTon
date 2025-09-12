from app.config import broker_router


async def make_notification(tg_id: int, text: str):
    await broker_router.broker.publish(
        {"tg_id": tg_id, "text": text},
        queue="notification",
        content_type="application/json",
    )
    return {"data": "OK"}