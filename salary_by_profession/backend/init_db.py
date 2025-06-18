import asyncio
from salary_by_profession.db.utils import insert_to_db


if __name__ == '__main__':
    asyncio.run(insert_to_db())
