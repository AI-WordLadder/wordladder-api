FROM python:3.7-alpine AS builder

RUN mkdir -p /usr/src/wordladder_api

WORKDIR /usr/src/wordladder_api

COPY requirements.txt /usr/src/wordladder_api/

RUN pip install --no-cache-dir -r requirements.txt

COPY run.sh /usr/src/wordladder_api/

CMD sh run.sh