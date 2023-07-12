FROM python:3.11-slim

ENV POETRY_HOME /opt/poetry
ENV PATH $POETRY_HOME/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    PYTHONPYCACHEPREFIX=/tmp/cpython \
    POETRY_VIRTUALENVS_CREATE=false

RUN mkdir /app && mkdir -p /opt && mkdir /.pytest_cache

RUN apt update && apt install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python && \
    chmod -R 777 /opt

RUN apt update -y -q \
    && apt install -y -q --no-install-recommends build-essential

COPY pyproject.toml ./
RUN poetry install

WORKDIR /app