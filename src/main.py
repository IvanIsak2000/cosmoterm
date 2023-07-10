import os
import sys
import argparse
import socket
from datetime import datetime
import logging
from rich.console import Console

console = Console(highlight=False)

logging.basicConfig(filename='client.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


class Client:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = client_socket 
        

    def start_client_part(self) -> None:
        self.client_socket.connect((self.host, self.port))  
        try:
            console.print(f'[yellow]Your friend with IP {self.host} online!')
            correct_response = self.send_and_get_response()

            if correct_response:
                logger.info('Connected')
                console.print('[green]Connection approved')  
                message = input("Enter your message: ")  
                self.message = message 
                self.send_message()
                current_time = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                console.print('[green]Message sent successfully!')
                logger.info(f'{self.host}: {self.message}')

            else:
                logger.error('Wrong token')
                console.print('[red]Wrong token!')

            self.client_socket.close()
            
        except KeyboardInterrupt:
            logger.info('User closed program')
            sys.exit()

        except Exception as e:
           logger.exception(e)
                

    def send_and_get_response(self) -> bool:
        self.client_socket.send(password.encode())
        response = self.client_socket.recv(1024).decode()
        return response == 'True'
    

    def send_message(self) -> None:
        self.client_socket.send(self.message.encode())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-a','--action', help='mode', default='send')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help="standart connection: python3 main.py  <-a send or --action send or without> <host> <port> <password>")


    parser.add_argument('host', type=str, help='user host')
    parser.add_argument('port', type=int, help='user port')
    parser.add_argument('password', type=int, help='session password')

    arg = parser.parse_args()
    
    if arg.action == 'send':
        password = str(arg.password)
        client = Client(arg.host, arg.port)
        client.start_client_part()