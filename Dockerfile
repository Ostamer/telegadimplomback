FROM nvidia/cuda:12.0.0-devel-ubuntu22.04

# Установка Python и необходимых инструментов
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка Python-пакетов
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    pip install --upgrade pip

WORKDIR /app

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install accelerate>=0.26.0 bitsandbytes

# Копирование приложения
COPY . .

# Запуск приложения
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
