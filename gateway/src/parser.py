from typing import Tuple

from logger import get_logger

logger = get_logger(__name__)


class ParseError(Exception):
    pass


def parse_message(raw: str) -> Tuple[str, float, str]:
    """
    Expected format:
        SENSOR_TYPE:VALUE:STUDENT_ID
    """
    logger.info(f"Parsing message: {raw}")
    parts = raw.strip().split(":")
    if len(parts) != 3:
        raise ParseError("invalid format (expected 3 fields: SENSOR_TYPE:VALUE:STUDENT_ID)")

    sensor_type, value_str, student_id = parts

    sensor_type = sensor_type.strip().upper()
    student_id = student_id.strip()

    if not sensor_type:
        raise ParseError("sensor type is empty")
    if not student_id:
        raise ParseError("student ID is empty")

    try:
        value = float(value_str.strip())
    except ValueError:
        raise ParseError("invalid numeric value")

    return sensor_type, value, student_id
