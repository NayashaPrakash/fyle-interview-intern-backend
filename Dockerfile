FROM python:3.8.16-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

#copy the source code into the container
COPY . .

#resert db
ENV FLASK_APP=core/server.py
RUN rm -f core/store.sqlite3
RUN flask db upgrade -d core/migrations/

CMD bash run.sh
