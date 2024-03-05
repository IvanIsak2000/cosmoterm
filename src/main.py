import argparse
import asyncio
import argparse
from PIL import Image

import secrets
import threading


from utils.logger import logger
from utils.server import Server
from utils.client import Client


def get_currently_token_to_conenct(host, port, key):
    """Типо получить текущий qr код с данными для подкчлюения"""
    qr_token = qrcode.make(f'{host} {port} {key}')
    qr_token.save("session_token.png")
    qr_token = Image.open('session_token.png')
    qr_token.show()


def generate_session_key() -> str:
    return secrets.token_urlsafe(69)


if __name__ == '__main__':

    output_lock = threading.Lock()

    logger.info('Program was start')
    server_part = Server()
    client_part = Client()

    client_part.start()
    server_part.start()
    
    client_part.join()
    server_part.join()
    