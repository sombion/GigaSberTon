from pydantic import BaseModel, Field
from datetime import datetime

class SApplicationsDeparture(BaseModel):
    applications_id: int = Field(...)
    departure_date: datetime = Field(...)