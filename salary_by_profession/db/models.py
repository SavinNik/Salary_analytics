from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Text, Float, ForeignKey

import datetime


class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self) -> dict:
        return {
            'id': self.id
        }


class Profession(Base):
    __tablename__ = 'professions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    vacancies: Mapped[list['Vacancy']] = relationship('Vacancy', back_populates='profession')

    @property
    def dict(self):
        return {
            'name': self.name
        }


class Vacancy(Base):
    __tablename__ = 'vacancies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vacancy: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    experience: Mapped[str] = mapped_column(String(200), nullable=True)
    employment: Mapped[str] = mapped_column(String(200), nullable=True)
    schedule: Mapped[str] = mapped_column(String(200), nullable=True)
    salary_from: Mapped[float] = mapped_column(Float, nullable=False)
    salary_to: Mapped[float] = mapped_column(Float, nullable=False)
    period_of_pay: Mapped[str] = mapped_column(String(200), nullable=True)
    currency: Mapped[str] = mapped_column(String(200), nullable=False)
    skills: Mapped[str] = mapped_column(Text, nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(String(50), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=True)
    responsibilities: Mapped[str] = mapped_column(Text, nullable=True)
    requirements: Mapped[str] = mapped_column(Text, nullable=True)
    position: Mapped[str] = mapped_column(String(200), nullable=True)
    education: Mapped[str] = mapped_column(Text, nullable=True)
    benefits: Mapped[str] = mapped_column(Text, nullable=True)
    industry: Mapped[str] = mapped_column(String(200), nullable=True)
    contact: Mapped[str] = mapped_column(String(200), nullable=True)

    profession_id: Mapped[int] = mapped_column(Integer, ForeignKey('professions.id'), index=True)
    profession: Mapped['Profession'] = relationship('Profession', back_populates='vacancies')


    @property
    def dict(self):
        return {
            'vacancy': self.vacancy,
            'company': self.company,
            'city': self.city,
            'country': self.country,
            'experience': self.experience,
            'employment': self.employment,
            'schedule': self.schedule,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'period_of_pay': self.period_of_pay,
            'currency': self.currency,
            'skills': self.skills,
            'text': self.text,
            'url': self.url,
            'date': self.date,
            'level': self.level,
            'responsibilities': self.responsibilities,
            'requirements': self.requirements,
            'position': self.position,
            'education': self.education,
            'benefits': self.benefits,
            'industry': self.industry,
            'contact': self.contact
        }
