import socket
import os
import sys
from datetime import datetime
import logging
from genp import password_generation
from PIL import Image   
import qrcode
import toml
from rich.console import Console


console = Console(highlight=False)

logging.basicConfig(filename='server.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


def check_token(conn: socket.socket, session_token: str) -> bool:
    get_client_token = conn.recv(1024).decode()
    if get_client_token == session_token:
        return True
    else:
        return False



def add_in_history(host: str, current_time: str, message: str) -> None:
    if not os.path.isfile('history.toml'):
        print('Файл не существовал, создан успешно.')
        create_history_file()
        
    time_and_message = {current_time: message}
    full_session_data = {host: time_and_message}

    time_and_messege = {}
    full_session_data = {}

    time_and_messege[current_time] = message
    full_session_data[address] = time_and_messege

    with open('history.toml', 'a') as file:
        toml.dump(full_session_data, file)


def create_history_file() -> None:
    with open('history.toml', 'w') as file:
        file.write('Created!\n')


def await_connection(session_token: str):
    global server_socket
    while True:
        try:
            console.print('[#9400D3]We are waiting for the connection...[#9400D3]')
            conn, address = server_socket.accept()
            console.print(f'[yellow]Connected with[yellow] {address}')
            send_response(conn, address, session_token)

        except socket.error as err:
            print(err)
            continue

def send_response(conn: socket.socket, address: tuple[str, int], session_token: str) -> None:
    is_correct_token = check_token(conn, session_token)

    if is_correct_token:

def send_response(conn: str, address: str, session_token: str) -> None:

    correct_token = check_token(conn, session_token)
    if correct_token :      
        response = 'True'
        conn.send(response.encode())
        console.print('[green]The token is correct, we are waiting for the message')  
        get_message(conn, address)

    else:
        response = 'False'
        conn.send(response.encode())
        console.print('[red]The client entered the wrong session token. Connection closed')
        logger.info(f'{address}: {response}') 
        conn.close()


def get_message(conn: socket.socket, address: tuple[str, int]) -> None:          
    message = conn.recv(1024).decode()
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    console.print(f"[{(address[0])}] [{current_time}]: " + str(message.split()[0]))
    add_in_history(address[0], current_time, message)  
    logger.info(f'{address}: {message} {True}')             

    conn.close()
    print('_____________________________')
    

def print_logo() -> None:
    with open('logo.txt') as logo:
        print(logo.read())


if __name__ == '__main__':

    try:
        start = input('Start server? (enter/ Ctrl + C)')

    except KeyboardInterrupt:
        print('\nThe program is stopped !')
        sys.exit()

    print_logo()    # выводит логотип в консоль

    host_ = socket.gethostbyname(socket.gethostname())
    port_ = 5000
    password = (password_generation(True, False, False, 15))
    session_token_ = host_ + str(port_) + str(password)

    print(f"""
    Your host: {host_}
    Your port: {port_}
    Password: {password}
    Session token: {host_} {port_} {password}
    -----------------------------------------
            """)

    qr_token = qrcode.make(f'{host_} {port_} {password}')
    qr_token.save("session_token.png")
    qr_token = Image.open('session_token.png')
    qr_token.show() 

    server_socket = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM
    )
    server_socket.bind((host_, port_))
    server_socket.listen(2)

    await_connection(session_token_)
