FROM registry.access.redhat.com/ubi8/python-38:latest

USER 0

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app.py /app/app.py
WORKDIR /app/

ENV PYTHONPATH=/app

USER 1001
