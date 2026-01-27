from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.models.input_file import InputFile

class InputFileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, filename: str, s3_path: str) -> InputFile:
        db_obj = InputFile(filename=filename, s3_path=s3_path, status="PENDING")
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: int) -> InputFile | None:
        result = await self.db.execute(select(InputFile).where(InputFile.id == id))
        return result.scalars().first()

    async def update_status(self, id: int, status: str, result_path: str = None):
        stmt = update(InputFile).where(InputFile.id == id).values(status=status)
        if result_path:
            stmt = stmt.values(result_s3_path=result_path)
        await self.db.execute(stmt)
        await self.db.commit()