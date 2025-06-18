import pandas as pd
import os
from pathlib import Path
from sqlalchemy.exc import IntegrityError
from .models import Profession, Vacancy
from .session import Session, init_orm


# Получаем абсолютный путь к файлу
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = os.path.join(BASE_DIR, "db", "Data.xlsx")

# Используем правильный путь
df = pd.read_excel(DATA_PATH, sheet_name="full_data_stage_1")

# Заполнение пропущенных значений пустыми строками
df = df.fillna("")

# Преобразование даты
df["date"] = pd.to_datetime(df["date"], errors='coerce')
df["date"] = df["date"].apply(lambda x: x.tz_localize(None) if pd.notna(x) and x.tz else x)

async def add_professions_and_vacancies(session):
    """ Функция добавляет профессии и вакансии в БД """
    professions = df["position"].unique()
    profession_map = {}

    # Добавление профессий
    for name in professions:
        profession = Profession(name=name)
        session.add(profession)
        try:
            await session.flush()
            profession_map[name] = profession.id
        except IntegrityError:
            await session.rollback()
            result = await session.execute(
                Profession.__table__.select().where(Profession.name == name)
            )
            profession = result.fetchone()
            profession_map[name] = profession.id

    # Добавление вакансий
    for _, row in df.iterrows():
        profession_id = profession_map.get(row["position"], None)
        date_parsed = row["date"] if pd.notna(row["date"]) else None

        vacancy = Vacancy(
            vacancy=row["vacancy"],
            company=row["company"],
            city=row["city"],
            country=row["country"],
            experience=row["experience"],
            employment=row["employment"],
            schedule=row["schedule"],
            salary_from=float(row["salary from"]),
            salary_to=float(row["salary to"]),
            period_of_pay=row["period of pay"],
            currency=row["currency"],
            skills=row["skills"],
            text=row["text"],  # Теперь не может быть NaN
            url=row["url"],
            date=date_parsed,
            level=row["level"],
            responsibilities=row["responsibilities"],
            requirements=row["requirements"],
            position=row["position"],
            education=row["education"],
            benefits=row["benefits"],
            industry=row["industry"],
            contact=row["contact"],
            profession_id=profession_id
        )
        session.add(vacancy)

    await session.commit()


async def insert_to_db():
    """ Функция добавляет данные в БД """
    await init_orm()
    async with Session() as session:
        try:
            await add_professions_and_vacancies(session)
            print("✅ Данные успешно добавлены в БД")
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при добавлении данных: {e}")
        finally:
            await session.close()