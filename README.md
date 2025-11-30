# README

# sensor-reporting-system

Distributed Systems Programming — Assignment 2
Student ID: **R00226564**



## Overview

This project implements a simple **distributed sensor reporting system** consisting of three services:

1. **Client (TCP)** — sends sensor readings to the gateway
2. **Gateway (TCP → gRPC bridge)** — validates socket input and forwards requests
3. **Worker (gRPC)** — validates sensor readings and returns a result

The system uses:

* TCP sockets (client -> gateway)
* gRPC (gateway -> worker)
* Docker + Docker Compose
* Custom network containing student ID: `dsp_net_R00226564`



## Folder Structure

```bash
project-root/
  client/
    src/
  gateway/
    src/
  worker/
    src/
  proto/
  config/
  docker/
    docker-compose.yml
  README.md
```


## How to Run the System


### 1. Start the Gateway + Worker (Docker Compose)

From the `docker/` directory:

```bash
cd docker
docker compose up --build
```

Expected output:

* Worker starts gRPC server on port **50051**
* Gateway listens for TCP connections on port **5050**

Leave this terminal running.



### 2. Run the Client (from host machine)

From the **project root**:

```bash
python3 client/src/client.py
```

You will be prompted:

```bash
Enter sensor type (TEMP/HUM/LIGHT):
Enter value:
```

Example:

```bash
TEMP
25
```

Expected:

```bash
Sent: TEMP:25:R00226564
Received: reading accepted
```



## Message Formats

### TCP Message (client -> gateway)

```bash
SENSOR_TYPE:VALUE:STUDENT_ID
```

Example:

```bash
TEMP:25:R00226564
```

Rules:

* Colon-separated
* Sensor types uppercase (TEMP, HUM, LIGHT)
* Value must be numeric
* Student ID always included



### gRPC Message (gateway → worker)

`ReadingRequest`:

| Field       | Type   | Description          |
| ----------- | ------ | -------------------- |
| sensor_type | string | TEMP/HUM/LIGHT       |
| value       | double | numeric reading      |
| student_id  | string | must include ID |

Worker returns a `ReadingResponse` with:

* `reading accepted`
* `reading invalid`
* `sensor type not supported`



## Failure Scenario

The failure scenario demonstrates **worker unavailable**.

### Steps:

1. System running (`docker compose up`)
2. Client sends a reading -> receives **reading accepted**
3. Stop the worker:

```bash
docker stop worker-service
```

4. Client sends the same reading again
5. Expected output:

```bash
Received: ERROR: worker unavailable
```

Gateway logs will show a gRPC connection failure.

This scenario should be included in:

* Screenshots
* Demo video
* Report



## Docker 

### Docker Services

| Service         | Port                    | Purpose                 |
| --------------- | ----------------------- | ----------------------- |
| worker-service  | 50051 (internal)        | gRPC validation service |
| gateway-service | 5050 (host -> container)| TCP server              |


### Custom Network

```bash
dsp_net_R00226564
```

Created automatically by Docker Compose.



## Requirements

Install PyYAML for client:

```bash
pip3 install PyYAML
```

(Docker handles all other dependencies.)



## Troubleshooting

### Worker dies immediately

Likely due to missing proto imports.
Rebuild:

```bash
docker compose down
docker compose up --build
```

### “worker unavailable” even when running

Check logs:

```bash
docker logs gateway-service
docker logs worker-service
```

### Proto changes not reflected

Rebuild images:

```bash
docker compose up --build
```



## Test end to end 

1. `docker compose up --build`
2. Run client: `python3 client/src/client.py`
3. Send sensor reading → accepted
4. Stop worker: `docker stop worker-service`
5. Send again → “ERROR: worker unavailable”

If all works, system is fully operational.
