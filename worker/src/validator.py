from typing import Dict, Any

from logger import get_logger

logger = get_logger(__name__)


class ValidationResult:
    def __init__(self, status_message: str):
        self.status_message = status_message


class ReadingValidator:
    def __init__(self, sensors_cfg: Dict[str, Any]):
        self.allowed_types = set(sensors_cfg.get("allowed_types", []))
        self.ranges = sensors_cfg.get("ranges", {})
        logger.info(
            f"Validator allowed_types={self.allowed_types}, ranges={self.ranges}"
        )

    def validate(self, sensor_type: str, value: float) -> ValidationResult:
        sensor_type = sensor_type.upper()
        logger.info(f"Validating sensor_type={sensor_type}, value={value}")

        if sensor_type not in self.allowed_types:
            logger.info("Sensor type not supported")
            return ValidationResult("sensor type not supported")

        sensor_ranges = self.ranges.get(sensor_type)
        if sensor_ranges:
            min_val = sensor_ranges.get("min")
            max_val = sensor_ranges.get("max")
            if min_val is not None and value < min_val:
                logger.info("Value below allowed range")
                return ValidationResult("reading invalid")
            if max_val is not None and value > max_val:
                logger.info("Value above allowed range")
                return ValidationResult("reading invalid")

        logger.info("Reading accepted")
        return ValidationResult("reading accepted")
