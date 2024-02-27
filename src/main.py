import os
import sys
import argparse
import socket
from datetime import datetime
from rich.console import Console
import asyncio

import apscheduler
import argparse
from PIL import Image
import qrcode
import toml
from rich.console import Console
import socket
import threading
import time
import qrcode
import secrets
from apscheduler.schedulers.background import BackgroundScheduler

from utils.logger import logger
from server import Server
from client import Client


def get_currently_token_to_conenct(host, port, key):
    """Типо получить текущий qr код с данными для подкчлюения"""
    qr_token = qrcode.make(f'{host} {port} {key}')
    qr_token.save("session_token.png")
    qr_token = Image.open('session_token.png')
    qr_token.show()


def generate_session_key() -> str:
    return secrets.token_urlsafe(69)


def client_part_task():
    client_part = Client()
    scheduler.add_job(client_part.listen_messages, 'interval', seconds=1)
    scheduler.start()



def server_part_task(host, port, key):
    """Таска от сервера"""
    server_part = Server()
    scheduler.add_job(server_task.await_connection, 'interval', seconds=1)
    scheduler.start()



if __name__ == '__main__':
    
    logger.info('Program was start')
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(server_part_task),
        loop.create_task(client_part_task)
    ]
    loop.run_until_complete(asyncio.gather(*tasks))

  