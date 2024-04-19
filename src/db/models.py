from sqlalchemy import Column, DateTime, Integer, String, func
from src.db.database import Database

class Result(Database.Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    sentiment = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
