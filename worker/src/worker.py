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
