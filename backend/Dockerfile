FROM python:3.13-slim

# Устанавливаем зависимости для libreoffice
RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh