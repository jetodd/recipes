FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8080

# replace APP_NAME with module name
CMD ["./debug.sh"]
