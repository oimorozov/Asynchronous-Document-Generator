from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.models.base import Base

class InputFile(Base):
    __tablename__ = "input_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    s3_path = Column(String)
    status = Column(String, default="PENDING")
    result_s3_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())