import os
import sys
import socket
from datetime import datetime
import logging
from rich.console import Console


console = Console(highlight=False)

logging.basicConfig(filename='client.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


client_socket: socket.socket   


def connection_to_server_part(host: str, port: int) -> None:
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        console.print(f'[yellow]Your friend with IP {host} online!')

        correct_response = send_and_get_response()

        if correct_response:
            console.print('[green]Connection approved')  
            message = input("Enter your message: ")                      
            send(message)
            current_time = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))  # не используется
            console.print('[green]Message sent successfully!')
            logger.info(f'{host}: {message}')

        else:
            console.print('[red]Wrong token!')

        client_socket.close()
        
    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
        print(e)
            

def send_and_get_response() -> bool:
    global client_socket

    client_socket.send(token.encode())
    response = client_socket.recv(1024).decode()
    if response == "True":
        return True
    else:
        return False


def send(message: str) -> None:
    global client_socket

    client_socket.send(message.encode())


if __name__ == '__main__':
    try:
        action = sys.argv

        if  action[1] == '--send':
            token = str(action[2] + action[3] + action[4])
            connection_to_server_part(str(action[2]), int(action[3]))

        else:
            input("""
Error when entering a command!
Available commands:
python main.py --set (configures the server.py in a startup, so that the server is restarted when the PC is turned on)
python main.py --send <host> <port> <password>""")

    except IndexError:
        input("""
The correct entry is:
python main.py --set 
python main.py --send <host> <port> <password>""")

    except Exception as err:
        input(err)
