FROM python:3.7-alpine 

RUN mkdir -p /wordladder_api

WORKDIR /wordladder_api

COPY . .

RUN pip install --no-cache-dir -r /wordladder_api/requirement.txt

EXPOSE 8000:8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]