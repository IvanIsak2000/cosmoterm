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
import psutil

import threading

from utils.logger import logger


class Server:
    """Класс будет ожидать сообщения от других пользователй"""

    def __init__(self):
        threading.Thread.__init__(self)
        console = Console(highlight=False)
        self.console= console
        server_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM)
        
        self.server_socket = server_socket
        host, port = 'localhost', 8000
        self.host = host
        self.port = port 
        print('start')

    def start(self) -> None:
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            self.console.print('[green]You are ready to get message!')

        except OSError as err:
            if err.errno == 98:
                self.kill_port()
                pass



        while True:
            try:

                conn, address = self.server_socket.accept()
                self.conn = conn
                self.address = address
                # self.console.print(f'[yellow]Connected with[yellow] {address}')
                self.send_response()

            except KeyboardInterrupt:
                logger.info('Program was closed when awaiting connection')
                print('Bye!')
                sys.exit()

            # except Exception as e:
            #     logger.exception(e)
            #     sys.exit()

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

    def key_is_valid(self) -> bool:
        """Get sender's key and check valid or not"""
        get_client_key = self.conn.recv(1024).decode()
        return get_client_key == self.key
    
    def kill_port(self):
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                for conn in proc.info['connections']:
                    if conn.laddr.port == self.port:
                        pid = proc.info['pid']
                        process = psutil.Process(pid)
                        process.terminate()
                        print('port was killed')
        except TypeError:
            raise 'Sorry, but program cannot use it port. Kill an app that using port. Maybe it can be ncat'

