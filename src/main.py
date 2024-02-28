import argparse
from rich.console import Console
import asyncio
import apscheduler
import argparse
from PIL import Image
from rich.console import Console

import secrets
from apscheduler.schedulers.background import BackgroundScheduler
from abc import ABC, abstractmethod

from utils.logger import logger
from utils.server import Server
from utils.client import Client

class Messanger(ABC):
    def __init__(self) -> None:
        pass


    @abstractmethod
    def get_currently_token_to_conenct(host, port, key):
        """Типо получить текущий qr код с данными для подкчлюения"""
        qr_token = qrcode.make(f'{host} {port} {key}')
        qr_token.save("session_token.png")
        qr_token = Image.open('session_token.png')
        qr_token.show()


    @abstractmethod
    def generate_session_key() -> str:
        return secrets.token_urlsafe(69)


    @abstractmethod
    def client_part_task():
        client_part = Client()
        scheduler.add_job(client_part.start_client_part, 'interval', seconds=1)
        scheduler.start()


    @abstractmethod
    def server_part_task(host, port, key):
        """Таска от сервера"""
        server_part = Server()
        scheduler.add_job(server_task.start_messaging, 'interval', seconds=1)
        scheduler.start()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()



    parser = argparse.ArgumentParser(add_help=False)

    subparser = parser.add_subparsers()
    mode = subparser.add_parser('-a','--action', help='mode', default='send')


    # parser.add_argument('-m','--message', type=str, help='write your message with start program', default=None)    
    # parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help="standart connection: python3 main.py  <-a send or --action send or without> <host> <port> <password>")

    # parser.add_argument('host', type=str, help='user host')
    # parser.add_argument('port', type=int, help='user port')
    # parser.add_argument('password', type=int, help='session password')
   

    arg = parser.parse_args()
    
    

    if mode == 'get':
        messanger = Messanger()
        logger.info('Program was start')
        print('print !h ro print all commands!')
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(messanger.server_part_task),
            loop.create_task(messanger.client_part_task)
        ]
        loop.run_until_complete(asyncio.gather(*tasks))
    else:
        raise

    