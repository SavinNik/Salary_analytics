from fastapi import FastAPI
from salary_by_profession.app.endpoints import router
from salary_by_profession.core.lifespan import lifespan
import uvicorn
from salary_by_profession.db.utils import insert_to_db
import asyncio


app = FastAPI(
    title='API for salary_by_profession',
    description='Get professions and salary by profession',
    lifespan=lifespan
)

app.include_router(router, prefix='/api/v1')


if __name__ == "__main__":
    # asyncio.run(insert_to_db()) <- для заполнения БД
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


