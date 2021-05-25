FROM python:3
RUN mkdir -p /braun
WORKDIR /braun
COPY pyproject.toml poetry.lock /braun/
RUN pip3 install poetry
ENV POETRY_VIRTUALENVS_CREATE false
RUN poetry install --no-root
COPY . /braun
RUN poetry install
