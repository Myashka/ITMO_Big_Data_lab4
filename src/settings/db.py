from datetime import datetime

from src.settings.base import ExtraFieldsNotAllowedBaseModel


class DBResult(ExtraFieldsNotAllowedBaseModel):
    id: int
    message: str
    sentiment: str
    created_at: datetime

    class Config:
        orm_mode = True
