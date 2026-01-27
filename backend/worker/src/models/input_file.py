from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.database import Base

class InputFile(Base):
    __tablename__ = "input_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    s3_path: Mapped[str]
    status: Mapped[str]
    result_s3_path: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    