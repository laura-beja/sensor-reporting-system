import os
import sys

# Add src and proto folder to PYTHONPATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROTO_DIR = os.path.join(CURRENT_DIR, "proto")
# Making sure Python can import sensor_pb2 / sensor_pb2_grpc
sys.path.append(CURRENT_DIR)
sys.path.append(PROTO_DIR)

from logger import get_logger
from config_loader import get_worker_config
from validator import ReadingValidator
from grpc_server import serve

logger = get_logger(__name__)


def main():
    worker_cfg, sensors_cfg, student_id = get_worker_config()
    grpc_port = worker_cfg["grpc_port"]

    logger.info(f"Worker starting with student ID: {student_id}")

    validator = ReadingValidator(sensors_cfg)
    serve(grpc_port, validator, student_id)


if __name__ == "__main__":
    main()
