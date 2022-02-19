FROM python:3.7-alpine3.15
RUN apt-get build-dep python-psycopg2 && apt install python3-psycopg2

WORKDIR /app/

ADD ./Pipfile* /app/
RUN python -m pipenv install --system --ignore-pipfile

COPY . /app/
