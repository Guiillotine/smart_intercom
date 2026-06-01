FROM python:3.12

WORKDIR /app/

RUN pip install poetry==2.0.1

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY . .
ENV PYTHONPATH=.

RUN chmod +x ./scripts/backend-dev-start.sh

CMD ["bash", "./scripts/backend-dev-start.sh" ]
