from sqlalchemy.orm import (
    Mapped, mapped_column
)

from src.db.database import Base

class InputFile(Base):
    __tablename__ = "input_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    