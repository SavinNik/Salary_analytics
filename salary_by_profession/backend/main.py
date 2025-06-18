from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import router
from core.lifespan import lifespan
import uvicorn
from db.utils import insert_to_db
import asyncio


app = FastAPI(
    title='API for salary_by_profession',
    description='Get professions and salary by profession',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],   # Разрешенные источники
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

app.include_router(router, prefix='/api/v1')


if __name__ == "__main__":
    # asyncio.run(insert_to_db()) <- для заполнения БД
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


