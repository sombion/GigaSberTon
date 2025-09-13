from datetime import datetime
from pydantic import BaseModel, Field


class SCreateConclusion(BaseModel):
    applications_id: int = Field(..., description="Id заявление заявителя")
    date: datetime = Field(..., description="Дата заключения")
    chairman_id: int = Field(..., description="id председателя комиссии")
    members_id: list = Field(..., description="id членов комиссии")
    justification: str = Field(..., description="Принятие заключения о ...")
    documents: str = Field(..., description="Рассмотренные документы")
    conclusion: str = Field(..., description="По результам обследования")