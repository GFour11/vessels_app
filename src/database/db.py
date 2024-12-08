import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE = os.getenv("db")


engine = create_async_engine(DATABASE, echo=True)

# Конфігурація асинхронної сесії
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Функція для отримання сесії
async def get_db():
    async with async_session() as session:
        yield session