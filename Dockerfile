FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (important)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .
# 👇 YAHAN LIKHNA HAI (COPY ke baad)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# 👇 LAST LINE
CMD gunicorn knowbase_ai.wsgi:application --bind 0.0.0.0:$PORT