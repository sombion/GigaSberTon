from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from datetime import datetime, timezone


class SCreateApplications(BaseModel):
    tg_id: int = Field(...),
    fio: str = Field(...),
    phone: str = Field(...),
    email: str = Field(...),
    cadastral_number: str = Field(...),
    address: str = Field(...),

class SApplicationsDeparture(BaseModel):
    applications_id: str = Field(...)
    departure_date: datetime = Field(...)

    @field_validator("departure_date", mode="before")
    @classmethod
    def parse_iso_datetime(cls, v):
        if isinstance(v, str):
            # Z заменяем на +00:00, чтобы fromisoformat понял
            if v.endswith("Z"):
                v = v[:-1] + "+00:00"
            dt = datetime.fromisoformat(v)
            # Если нет tzinfo — добавляем UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            # Конвертируем в UTC
            return dt.astimezone(timezone.utc)
        return v