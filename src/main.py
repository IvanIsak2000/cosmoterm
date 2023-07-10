import os
import sys
import argparse
import socket
from datetime import datetime
import logging
from rich.console import Console


console = Console(highlight=False)

logging.basicConfig(filename='client.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


def connection_to_server_part(host: str, port: int) -> None:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        console.print(f'[yellow]Your friend with IP {host} online!')

        correct_response = send_and_get_response(client_socket)

        if correct_response:
            console.print('[green]Connection approved')  
            message = input("Enter your message: ")                      
            send(client_socket, message)
            current_time = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            console.print('[green]Message sent successfully!')
            logger.info(f'{host}: {message}')

        else:
            console.print('[red]Wrong token!')

        client_socket.close()
        
    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
        print(e)
            

def send_and_get_response(client_socket: socket.socket) -> bool:
    client_socket.send(password.encode())
    response = client_socket.recv(1024).decode()
    return response == 'True'
  

def send(client_socket: socket.socket, message: str) -> None:
    client_socket.send(message.encode())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-a','--action', help='mode', default='send')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help="python3 main.py <host> <port> <password>")


    parser.add_argument('host', type=str, help='user host')
    parser.add_argument('port', type=int, help='user port')
    parser.add_argument('password', type=int, help='session password')

    arg = parser.parse_args()
    
    if arg.action == 'send':
        password = str(arg.password)
        connection_to_server_part(arg.host, arg.port)

