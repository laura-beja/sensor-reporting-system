FROM python:3.12-slim

WORKDIR /app

COPY client/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY config /app/config
COPY client/src /app/client/src

CMD ["python", "-u", "client/src/client.py"]
