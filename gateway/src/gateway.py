from logger import get_logger
from config_loader import get_gateway_config
from grpc_client import WorkerClient
from tcp_server import TCPServer
from parser import parse_message, ParseError

import grpc

logger = get_logger(__name__)


def handle_message(worker_client: WorkerClient, raw_message: str) -> str:
    sensor_type, value, student_id = parse_message(raw_message)

    try:
        status = worker_client.process_reading(sensor_type, value, student_id)
        return status
    except grpc.RpcError as e:
        logger.error(f"gRPC error talking to worker: {e}")
        return "ERROR: worker unavailable"
    except Exception as e:
        logger.error(f"Unexpected error talking to worker: {e}")
        return "ERROR: worker unavailable"


def main():
    gateway_cfg, student_id = get_gateway_config()
    listen_host = gateway_cfg["listen_host"]
    tcp_port = gateway_cfg["tcp_port"]
    worker_host = gateway_cfg["worker_host"]
    worker_port = gateway_cfg["worker_port"]

    logger.info(f"Gateway starting with student ID: {student_id}")
    logger.info(f"Connecting to worker at {worker_host}:{worker_port}")

    worker_client = WorkerClient(worker_host, worker_port)

    server = TCPServer(
        host=listen_host,
        port=tcp_port,
        handler=lambda raw: handle_message(worker_client, raw),
    )

    server.start()


if __name__ == "__main__":
    main()
