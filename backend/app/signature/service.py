from datetime import datetime
from app.applications.dao import ApplicationsDAO
from app.applications.models import Applications
from app.conclusion.dao import ConclusionDAO
from app.conclusion.models import Conclusion
from app.notification.dao import NotificationDAO
from app.notification.service import make_notification
from app.signature.dao import SignatureDAO
from app.signature.models import Signature


async def all():
    signature_data = await SignatureDAO.all()
    return {"count": len(signature_data), "signatures": signature_data}


async def update_signature(users_id: int, conclusion_id: int):
    signature_data: Signature = await SignatureDAO.find_one_or_none(
        users_id=users_id, conclusion_id=conclusion_id
    )

    if signature_data.signed:
        raise {"datail": "Документ уже подписан"}

    signature_data: Signature = await SignatureDAO.update(signature_data.id)

    conclusion_data: Conclusion = await ConclusionDAO.find_one_or_none(id=conclusion_id)

    if not conclusion_data:
        raise {"detail": "Заявление комиссии не найдено"}

    applications_data: Applications = await ApplicationsDAO.find_one_or_none(
        id=conclusion_data.applications_id
    )

    # Проверка что все подписали заявление
    conclusion_data_list = await SignatureDAO.find_all(conclusion_id=conclusion_id)
    signed_all = True
    for conclusion_user in conclusion_data_list:
        if conclusion_user["signed"] == False:
            signed_all = False
            break

    if signed_all:
        # Уведомление для пользователя
        for conclusion_user in conclusion_data_list:
            await NotificationDAO.add(
                user_id=int(conclusion_user["users_id"]),
                text=f"Все члены комисси подписали заявление №{conclusion_id}",
            )
            await make_notification(
                tg_id=applications_data.tg_id,
                text=f"Работы по вашему заявлению №{conclusion_id} завершены, с результатами заявления комиссии можете ознакомится написав команду '/current {applications_data.id}'",
            )

    return {"detail": "Заявление успешно подписано"}


async def search_signature(text: str):
    signatures_data = await SignatureDAO.search(text)
    return {"count": len(signatures_data), "signatures": signatures_data}


async def filter_signature(
    street: str | None,
    date_from: datetime | None,
    date_to: datetime | None,
):
    signatures_data = await SignatureDAO.filter(street, date_from, date_to)
    return {"count": len(signatures_data), "signatures": signatures_data}
