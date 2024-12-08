import sys
import asyncio
from fastapi import FastAPI
import uvicorn
from src.routs.customers_operations import router

app = FastAPI()

# Підключення роутів
app.include_router(router)
if sys.platform == "win64":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# # Ініціалізація бази даних
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# Запуск FastAPI
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)