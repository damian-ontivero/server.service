FROM python:3.11.6-alpine3.18

RUN apk update
RUN apk upgrade

RUN mkdir -p /app

WORKDIR /app

COPY ./st_server /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "st_server.server.infrastructure.ui.api.main:app", "--host", "0.0.0.0", "--port", "4003"]
