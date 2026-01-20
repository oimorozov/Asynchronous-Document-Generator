from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped, mapped_column
)

from src.models.base import Base

class OutputFile(Base):
    __tablename__ = "output_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    input_file_id: Mapped[int] = mapped_column(ForeignKey('input_files.id'))