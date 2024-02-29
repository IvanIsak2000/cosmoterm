import argparse
from rich.console import Console
import asyncio
import argparse
from PIL import Image
from rich.console import Console
import argparse
import curses

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


def server():
    server_part = Server() 
    server_part.start()


def client():
    client_part = Client()
    client_part.start()

def print(window_id: int,  text: str, color_id: int):
    curses.start_color()
    #color, used by id: 1, 2, ...
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)

    if window_id == 1:
        screen.addstr(1, 0, text+'\n', curses.color_pair(1) | curses.A_NORMAL)

    if window_id == 2:
        screen.addstr(1, 50, text+'\n', curses.color_pair(2)| curses.A_NORMAL)



if __name__ == '__main__':

    screen = curses.initscr()

    # Change style: bold, highlighted, and underlined text
    print(1, text='Server window!', color_id=1)
    print(2, text='Client window!', color_id=2)
    print(2, text='Client window!', color_id=2)
    # print(1, text='1', color_id=2)

    try:
        screen.refresh()
        curses.napms(5000)
        curses.endwin()
    except KeyboardInterrupt:
        pass





    # logger.info('Program was start')


   
    # arg = parser.parse_args()
    

    # t1 = threading.Thread(target=server)
    # t2 = threading.Thread(target=client)
    
    # t1.start()
    # t2.start()
    

