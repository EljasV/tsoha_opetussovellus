FROM python:3.10-alpine

RUN apk add postgresql-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

COPY src/ src/

ENV FLASK_APP=src/app.py

CMD ["flask","run", "--host=0.0.0.0"]