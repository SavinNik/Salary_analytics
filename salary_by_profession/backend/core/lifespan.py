from contextlib import asynccontextmanager

from fastapi import FastAPI
from db.session import init_orm, close_orm
from core.cache import init_cache, close_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Функция для инициализации и закрытия кэша и БД """
    await init_cache()
    await init_orm()

    yield

    await close_cache()
    await close_orm()
