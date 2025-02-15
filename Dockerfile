FROM python:3.7-alpine 

RUN mkdir -p /usr/src/wordladder_api

WORKDIR /usr/src/wordladder_api

COPY requirements.txt /usr/src/wordladder_api/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]