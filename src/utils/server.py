#!/usr/bin/python3

import socket
from datetime import datetime
import secrets

import threading
import psutil
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.application.current import get_app
from cryptography.fernet import Fernet

try:
    from utils.logger import logger
except ModuleNotFoundError:
    from logger import logger


class Server:
    """Class that will wait messages, process the connection and print the message"""

    def __init__(self):
        logger.info('______________________________________________________\n')
        logger.info('Class __init__ start')
        threading.Thread.__init__(self)

        server_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM)
        self.server_socket = server_socket

        host = 'localhost'
        self.host = host

        port = 8001
        self.port = port

        public_key = Fernet.generate_key()
        logger.info(public_key)
        self.public_key = public_key

    def get_status(self):
        return f' Server work on {self.host, self.port}'
        
    def get_key_from_sender(self) -> str:
        """Get sender's key"""
        try:
            get_client_key = self.conn.recv(1024).decode()
            return get_client_key
        except Exception as e:
            logger.error(e)
            get_app().exit()  

    def sender_key_is_valid(self, public_key: str, key: str) -> bool:
        """Check sender key is valid or not"""
        return public_key == key

    def start(self) -> str:
        """Main function of server part.\n
        Does:
        1. Starts server
        2. Waits sender message
        3. Checks sender's key for validity
        4. If key is valid, sending the sender permission to send the message
        5. Returns message
        """
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            logger.info(f'Server part is listening {self.host, self.port}')
        except OSError as err:
            logger.info(f'Port  {self.host, self.port}')
            if err.errno == 98:
                self.kill_port()
                logger.info('Kill port')
                self.server_socket.bind((self.host, self.port))
                self.server_socket.listen()
        except KeyboardInterrupt:
            get_app().exit()
        except Exception as e:
            logger.error(e)
            get_app().exit()

        while True:
            try:
                conn, address = self.server_socket.accept()
                self.conn = conn
                self.address = address
                print(f'Connected with {self.address}')
                sender_key: bool = self.get_key_from_sender()

                if self.sender_key_is_valid(self.public_key, sender_key):
                    print('Key is valid')
                    self.send_response(True)
                    self.get_message()
                
                return 'Connection refused. Key is not valid'
            except KeyboardInterrupt:
                logger.info('Program was close')
                self.conn.close()
                get_app().exit()
            except Exception as e:
                logger.error(e)
                get_app().exit()
         
    def send_response(self, response: bool) -> None:
        """
        Sending the sender permission to send the message
        """
        try:
            if response:
                self.conn.send('True'.encode())
                logger.info(f'Send True resonse to sender {self.host}:{self.port}')
            self.conn.send('False'.encode())
        except KeyboardInterrupt:
            get_app().exit()

    def get_message(self) -> str:
        """Get sender's message and return that with his socket and time"""
        try:
            message = self.conn.recv(1024).decode()
            self.message = message
            current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.current_time = current_time
            logger.info(f'{self.address}: {message} {True}')
            self.conn.close()
            return (
                f"[{(self.address)}] [{self.current_time}]: " + str(self.message.split()[0]))
        except Exception as e:
            logger.error(e)
            get_app().exit()

    def kill_port(self):
        """Frees port for using"""
        for proc in psutil.process_iter():
            try:
                connections = proc.connections()
                for conn in connections:
                    if conn.laddr.port == self.port:
                        proc.kill()
                        print(f"Process with port {self.port} killed successfully.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            except Exception as e:
                logger.error(e)
                get_app().exit()
