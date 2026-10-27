FROM python:3.13-alpine

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

COPY . .

RUN uv sync --frozen --no-dev

ENV PYTHONUNBUFFERED=1
