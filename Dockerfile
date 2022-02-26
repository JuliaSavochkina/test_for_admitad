FROM python:3.7-alpine3.7
RUN apk update && apk add libpq && \
    apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev
RUN pip install psycopg2
RUN python -m pip install pipenv==2022.1.8

WORKDIR /app/

ADD ./Pipfile* /app/
RUN python -m pipenv install

COPY . /app/
