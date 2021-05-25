FROM python:3
RUN mkdir -p /fastapi-monitor
WORKDIR /fastapi-monitor
COPY pyproject.toml poetry.lock /fastapi-monitor/
RUN pip3 install poetry
ENV POETRY_VIRTUALENVS_CREATE false
RUN poetry install --no-root
COPY . /fastapi-monitor
RUN poetry install
