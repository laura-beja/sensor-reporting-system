import os
import socket
import yaml

from logger import get_logger

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "config.yaml")
logger = get_logger(__name__)


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def build_message(sensor_type: str, value: str, student_id: str) -> str:
    # Expecting uppercase sensor type and numeric value
    sensor_type = sensor_type.strip().upper()
    value = value.strip()
    return f"{sensor_type}:{value}:{student_id}"


def send_reading(host: str, port: int, message: str) -> str:
    logger.info(f"Connecting to gateway at {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        logger.info(f"Sending message: {message}")
        sock.sendall(message.encode("utf-8"))
        data = sock.recv(1024)
    response = data.decode("utf-8").strip()
    logger.info(f"Received response: {response}")
    return response


def main():
    config = load_config()
    gateway_cfg = config["gateway"]
    student_id = config["student_id"]

    host = "localhost"
    port = gateway_cfg["tcp_port"]

    print("=== Sensor Client (TCP) ===")
    print(f"Using student ID: {student_id}")
    print(f"Connecting to gateway at {host}:{port}")

    while True:
        sensor_type = input("Enter sensor type (TEMP/HUM/LIGHT): ").strip().upper()
        value = input("Enter value: ").strip()

        message = build_message(sensor_type, value, student_id)

        try:
            response = send_reading(host, port, message)
            print(f"\nSent:     {message}")
            print(f"Received: {response}\n")
        except Exception as e:
            logger.error(f"Error communicating with gateway: {e}")
            print(f"Error: {e}")

        again = input("Send another? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting client.")
            break


if __name__ == "__main__":
    main()
