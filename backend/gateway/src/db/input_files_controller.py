from src.db.database import session_factory

from src.models.input_file import InputFile

async def save_input_file(filename: str):

    new_input_file = InputFile(
        filename=filename
    )

    async with session_factory() as session:
        session.add(new_input_file)
        print(f"DATABASE-INPUT-FILE: {new_input_file}")
        await session.commit()
