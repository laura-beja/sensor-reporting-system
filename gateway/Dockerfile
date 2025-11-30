FROM python:3.12-slim

WORKDIR /app

# Install build deps for grpcio-tools
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 1. copy config and proto
COPY config /app/config
COPY proto /app/proto

# 2. copy gateway code FIRST
COPY gateway/src /app/gateway/src

# 3. NOW generate gRPC (write into the already-existing proto folder)
RUN python -m grpc_tools.protoc \
      -I /app/proto \
      --python_out=/app/gateway/src/proto \
      --grpc_python_out=/app/gateway/src/proto \
      /app/proto/sensor.proto


WORKDIR /app/gateway
CMD ["python", "-u", "src/gateway.py"]
