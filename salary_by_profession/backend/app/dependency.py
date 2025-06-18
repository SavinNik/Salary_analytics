from sqlalchemy.ext.asyncio import AsyncSession
from salary_by_profession.db.session import Session
from typing import Annotated
from fastapi import Depends

async def get_session() -> AsyncSession:
    """ Получение сессии """
    async with Session() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]