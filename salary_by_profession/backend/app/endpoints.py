from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.sql.functions import percentile_cont

from .schemas import ProfessionsResponse, SalaryResponse
from fastapi_cache.decorator import cache
from .dependency import SessionDependency
from backend.db.models import Profession, Vacancy


router = APIRouter()

@router.get('/professions/',
         response_model=ProfessionsResponse,
         summary='Список IT профессий',
         description='Возвращает список IT профессий')
@cache(expire=360)
async def get_professions(session: SessionDependency) -> ProfessionsResponse:
    """ Функция возвращает список IT профессий """
    # Получаем все профессии
    result = await session.execute(select(Profession.name))
    professions = result.scalars().all()
    return ProfessionsResponse(professions=professions)


@router.get('/salary/{profession_name}',
         response_model=SalaryResponse,
         summary='Средняя зарплата по профессии',
         description='Возвращает среднюю зарплату по IT профессии')
@cache(expire=360)
async def get_salary(profession_name: str, session: SessionDependency) -> SalaryResponse:
    """ Функция возвращает зарплату по IT профессии """
    # Получаем профессию
    result = await session.execute(
        select(Profession).where(Profession.name == profession_name)
    )
    profession = result.scalar_one_or_none()
    
    if profession:
        # Получаем все вакансии для профессии
        result = await session.execute(
            select(percentile_cont(0.5).within_group(Vacancy.salary_from), percentile_cont(0.5).within_group(Vacancy.salary_to))
            .where(Vacancy.profession_id == profession.id)
        )
        vacancies = result.all()

        
        if not vacancies:
            raise HTTPException(
                status_code=404,
                detail=f"Для профессии '{profession_name}' не найдено данных о зарплатах."
            )
        
        # # Извлекаем зарплаты из вакансий
        # salaries = []
        # for salary_from, salary_to in vacancies:
        #     if salary_from:
        #         salaries.append(salary_from)
        #     if salary_to:
        #         salaries.append(salary_to)
        #
        # if not salaries:
        #     raise HTTPException(
        #         status_code=404,
        #         detail=f"Для профессии '{profession_name}' не найдено данных о зарплатах."
        #     )
        #
        # # Сортируем зарплаты для расчета персентилей
        # salaries_sorted = sorted(salaries)
        # n = len(salaries_sorted)
        #
        # # Рассчитываем индексы для 5-го и 95-го персентилей
        # idx_5 = int(0.05 * n)
        # idx_95 = int(0.95 * n) - 1  # -1 так как индексация с 0
        #
        # # Получаем значения персентилей
        # salary_5th = salaries_sorted[idx_5] if n > 0 else 0
        # salary_95th = salaries_sorted[idx_95] if n > 0 else 0
        
        return SalaryResponse(
            profession=profession_name,
            salary_from=round(vacancies[0][0], 2),
            salary_to=round(vacancies[0][1], 2),
            currency='руб.'
        )
    
    raise HTTPException(
        status_code=404,
        detail="Профессия не найдена. Посмотрите список доступных профессий на http://127.0.0.1:8000/professions/."
    )
