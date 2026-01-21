from sqlalchemy.orm import (
    Mapped, mapped_column
)

from src.models.Base import Base

class InputFile(Base):
    __tablename__ = "input_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    