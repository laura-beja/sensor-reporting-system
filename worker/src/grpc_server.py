import grpc
from concurrent import futures

from logger import get_logger
from proto import sensor_pb2, sensor_pb2_grpc
from validator import ReadingValidator

logger = get_logger(__name__)


class SensorWorkerService(sensor_pb2_grpc.SensorWorkerServicer):
    def __init__(self, validator: ReadingValidator, student_id: str):
        super().__init__()
        self.validator = validator
        self.student_id = student_id

    def ProcessReading(self, request, context):
        logger.info(
            f"Received ProcessReading: sensor_type={request.sensor_type}, "
            f"value={request.value}, student_id={request.student_id}"
        )

        # Just log if student ID matches expected
        if request.student_id != self.student_id:
            logger.warning(
                f"Student ID mismatch: expected {self.student_id}, got {request.student_id}"
            )

        result = self.validator.validate(request.sensor_type, request.value)
        return sensor_pb2.ReadingResponse(status_message=result.status_message)


def serve(port: int, validator: ReadingValidator, student_id: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorWorkerServicer_to_server(
        SensorWorkerService(validator, student_id), server
    )
    server.add_insecure_port(f"[::]:{port}")
    logger.info(f"Starting gRPC worker server on port {port}")
    server.start()
    server.wait_for_termination()
