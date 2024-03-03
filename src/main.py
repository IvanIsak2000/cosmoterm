import argparse
from rich.console import Console
import argparse
from PIL import Image
from rich.console import Console
from prompt_toolkit import prompt
import time
from qrcode import make

import secrets
import threading

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import HSplit, Layout, VSplit
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea
from prompt_toolkit.shortcuts import button_dialog, yes_no_dialog
from prompt_toolkit.key_binding import KeyBindings

from utils.logger import logger
from utils.server import Server
from utils.client import Client

bindings = KeyBindings()


def get_currently_token_to_conenct(host, port, key):
    """Типо получить текущий qr код с данными для подкчлюения"""
    qr_token = make(f'{host} {port} {key}')
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


def write_message():
    text_area.text = 'Write you message!'


def _exit():
    result = yes_no_dialog(
        title='For exit',
        text='Do you want to close app?'
        ).run()
    if result:
        get_app().exit()


def send():
    text_area.text = 'was send!'


targets = ['Iwan', 'John', ]
exit_button = []


targets = [
    Button(name, handler=write_message) for name in targets
    ]

confirm = [Button("Send", handler=send), Button('Exit app', handler=_exit)]

text_area = TextArea(focusable=True)
root_container = Box(
    HSplit(
        [   
            Label(text="Press Up or Down keyboard to focus."),  
            VSplit(
                [
                    Box(   
                        body=HSplit(targets, padding=1),
                        padding=1,
                        style="class:left-pane"),
                    Box(body=Frame(text_area), 
                        padding=1, 
                        style="class:right-pane"),          
                    Box(body=Frame(HSplit(confirm, padding=1)),
                        padding=1,
                        style="class:right-pane")
                ])]))

layout1 = Layout(container=root_container, focused_element=targets[0])


style = Style(
    [
        ("left-pane", "bg:#E8E7E7 #000000"),
        ("right-pane", "bg:#E8E7E7 #000000"),
        ("button", "#000000"),
        ("button-arrow", "#000000"),
        ("button focused", "bg:#000000"),
        ("text-area focused", "bg:#ff0000"),
    ]
)

kb = KeyBindings()
kb.add("down",  'tab')(focus_next)
kb.add("up")(focus_previous)


tui = Application(
    layout=layout1, 
    key_bindings=kb, style=style, 
    full_screen=True
    )


def run_tui():
    tui.run()


if __name__ == '__main__':
    logger.info('Program was start')
    run_tui()


   
    # arg = parser.parse_args()
    

    # t1 = threading.Thread(target=server)
    # t2 = threading.Thread(target=client)
    
    # t1.start()
    # t2.start()
    

