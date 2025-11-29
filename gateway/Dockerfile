FROM python:3.12-slim

WORKDIR /app

# Install build deps for grpcio-tools
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy config and proto
COPY config /app/config
COPY proto /app/proto

# Generate gRPC Python code into gateway/src/proto
RUN mkdir -p /app/gateway/src/proto && \
    python -m grpc_tools.protoc \
      -I /app/proto \
      --python_out=/app/gateway/src/proto \
      --grpc_python_out=/app/gateway/src/proto \
      /app/proto/sensor.proto

# Copy gateway source
COPY gateway/src /app/gateway/src

WORKDIR /app/gateway
CMD ["python", "-u", "src/gateway.py"]
