FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_MODULE=app.main

CMD ["sh", "-c", "python -m ${APP_MODULE}"]
