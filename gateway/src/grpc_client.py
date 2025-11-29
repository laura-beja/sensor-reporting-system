import grpc
from logger import get_logger

from proto import sensor_pb2, sensor_pb2_grpc

logger = get_logger(__name__)


class WorkerClient:
    def __init__(self, host: str, port: int):
        target = f"{host}:{port}"
        logger.info(f"Creating gRPC channel to worker at {target}")
        self.channel = grpc.insecure_channel(target)
        self.stub = sensor_pb2_grpc.SensorWorkerStub(self.channel)

    def process_reading(self, sensor_type: str, value: float, student_id: str) -> str:
        request = sensor_pb2.ReadingRequest(
            sensor_type=sensor_type,
            value=value,
            student_id=student_id,
        )
        logger.info(
            f"Calling worker.ProcessReading(sensor_type={sensor_type}, value={value}, student_id={student_id})"
        )
        response = self.stub.ProcessReading(request)
        logger.info(f"Worker returned status_message={response.status_message}")
        return response.status_message
