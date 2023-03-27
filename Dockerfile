FROM python:3.10.6-alpine3.16

RUN apk update
RUN apk upgrade

RUN mkdir -p /app

WORKDIR /app

COPY ./st_support /app/st_support
COPY ./poetry.lock /app
COPY ./pyproject.toml /app
COPY ./README.md /app
COPY ./poetry.lock /app

RUN python -m pip install --upgrade pip

RUN pip install poetry

RUN poetry export --with-credentials --without-hashes --output requirements.txt

RUN pip install -r requirements.txt

CMD ["uvicorn", "st_support.application.app:app", "--host", "0.0.0.0", "--port", "16400"]
