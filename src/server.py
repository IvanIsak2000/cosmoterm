#!/usr/bin/python3

import socket
import os
import sys
import argparse
from datetime import datetime
import logging
from PIL import Image
import qrcode
import toml
from rich.console import Console
import secrets


from utils.logger import logger


class Server:
    """Класс будет ожидать сообщения от других пользователй"""

    def __init__(self):
        console = Console(highlight=False)
        server_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM)

        try:
            host, port = server_socket.getpeername()
            server_socket.bind((host, port))

        except OSError as err:
            if err.errno == 98:
                logger.exception(err)
                console.print(
'''[red]Oh no! This port using. 
Please close program and start as 
python3 server.py -p 5001 OR more ''')
                sys.exit()

        server_socket.listen()
        self.server_socket = server_socket

    def key_is_valid(self) -> bool:
        """Get sender's key and check valid or not"""
        get_client_key = self.conn.recv(1024).decode()
        return get_client_key == self.key

    # def add_in_history(self) -> None:
    #     if not os.path.isfile('history.toml'):
    #         self.create_history_file()

    #     time_and_messege = {}
    #     full_session_data = {}

    #     time_and_message = {self.current_time: self.message}
    #     full_session_data = {self.host: time_and_message}

    #     with open('history.toml', 'a') as file:
    #         toml.dump(full_session_data, file)
    def add_new_block():
        """Add new message's information block in blockchain"""
        ...

    # def create_history_file(self) -> None:
    #     with open('history.toml', 'w') as file:
    #         file.write('Created!\n')

    def await_connection(self) -> None:
        while True:
            try:
                self.console.print(
                    '\n[#9400D3]We are waiting for the connection...[#9400D3]')
                conn, address = self.server_socket.accept()
                self.conn = conn
                self.address = address
                self.console.print(f'[yellow]Connected with[yellow] {self.address}')
                self.send_response()

            except socket.error as err:
                logger.error(err)

            except KeyboardInterrupt:
                logger.info('Program was closed when awaiting connection')
                print('Bye!')
                sys.exit()

            except Exception as e:
                logger.exception(e)

    def send_response(self) -> None:

        if self.key_is_valid():
            response = 'True'
            self.conn.send(response.encode())
            self.console.print(
                '[green]The token is correct, we are waiting for the message')
            self.get_message()

        else:
            response = 'False'
            self.conn.send(response.encode())
            self.console.print(
                "[red]The client entered an invalid session key or did not enter a key. Connection closed ")
            logger.info(f'{self.address}: {response}')
            self.conn.close()

    def get_message(self) -> None:
        message = self.conn.recv(1024).decode()
        self.message = message
        current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.current_time = current_time
        self.console.print(
            f"[{(self.address)}] [{self.current_time}]: " + str(self.message.split()[0]))
        self.add_in_history()
        logger.info(f'{self.address}: {message} {True}')

        self.conn.close()
        print('_____________________________')
