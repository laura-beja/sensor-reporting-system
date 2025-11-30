FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY worker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY config /app/config
COPY proto /app/proto
COPY worker/src /app/worker/src

RUN python -m grpc_tools.protoc \
      -I /app/proto \
      --python_out=/app/worker/src/proto \
      --grpc_python_out=/app/worker/src/proto \
      /app/proto/sensor.proto


WORKDIR /app/worker
CMD ["python", "-u", "src/worker.py"]
