FROM python:3.11-slim

WORKDIR /app

# Копируем только зависимости сначала для кэширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/salary_by_profession/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]