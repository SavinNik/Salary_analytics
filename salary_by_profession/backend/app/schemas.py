from pydantic import BaseModel
from typing import List

class ProfessionsResponse(BaseModel):
    """ Класс для представления информации о профессии """
    professions: List[str]


class SalaryResponse(BaseModel):
    """ Класс для представления информации о средней зарплате по профессии """
    profession: str
    salary_from: float
    salary_to: float
    currency: str = 'руб.'