# Базовый образ
FROM python:3.13-slim

# Рабочая директория
WORKDIR /app

# Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY . .

# Переменная окружения для Python (чтобы вывод шел сразу в stdout)
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python", "main.py"]
