FROM node:21-alpine as frontend

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .

RUN npm run tailwind

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=frontend /app/recipes/static/recipes/style.css ./recipes/static/recipes/style.css

RUN python manage.py collectstatic --noinput

EXPOSE 8080

# replace APP_NAME with module name
CMD ["./debug.sh"]
