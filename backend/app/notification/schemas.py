from pydantic import BaseModel, Field


class SNotificationId(BaseModel):
    id: int = Field(...)

class SNotificationAll(BaseModel):
    id_list: list[int] = Field(...)