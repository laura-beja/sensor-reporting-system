import socket
import threading
from typing import Callable

from logger import get_logger
from parser import parse_message, ParseError

logger = get_logger(__name__)


class TCPServer:
    def __init__(self, host: str, port: int, handler: Callable[[str], str]):
        self.host = host
        self.port = port
        self.handler = handler

    def start(self):
        logger.info(f"Starting TCP server on {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logger.info("Gateway is listening for incoming client connections...")

            while True:
                conn, addr = s.accept()
                logger.info(f"Accepted connection from {addr}")
                thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                thread.start()

    def handle_client(self, conn: socket.socket, addr):
        with conn:
            try:
                data = conn.recv(1024)
                if not data:
                    logger.info(f"No data received from {addr}; closing connection.")
                    return

                raw_message = data.decode("utf-8").strip()
                logger.info(f"Received raw message from {addr}: {raw_message}")

                try:
                    response = self.handler(raw_message)
                except ParseError as e:
                    logger.error(f"Parse error: {e}")
                    response = f"ERROR: {str(e)}"
                except Exception as e:
                    logger.error(f"Unexpected error handling client message: {e}")
                    response = "ERROR: internal gateway error"

                conn.sendall(response.encode("utf-8"))
                logger.info(f"Sent response to {addr}: {response}")
            except Exception as e:
                logger.error(f"Error in client handler for {addr}: {e}")
