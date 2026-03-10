FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    libgdiplus \
    libx11-6 \
    libgl1 \
    libglib2.0-0 \
    libfontconfig1 \
    libpango-1.0-0 \
    libcairo2 \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    libicu-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn mysqlclient

COPY . .

CMD ["gunicorn", "PregRh.wsgi:application", "--bind", "0.0.0.0:8000"]
