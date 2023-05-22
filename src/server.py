import socket
import os
import sys
import time
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
logger=logging.getLogger(__name__)


def create_history_file():
    with open('history.toml', 'w') as file:
        file.write('Created!\n')

def add_in_history(host: str, current_time: str, message: str):

    time_and_messege = {}
    full_session_data = {}

    time_and_messege[current_time] = message
    full_session_data[host] = time_and_messege

    with open('history.toml', 'a') as file:
        toml.dump(full_session_data, file)




def await_connection(host: str, port: int, session_token: str):
    while True:
        try:
            console.print('[#9400D3]We are waiting for the connection...[#9400D3]')
            conn, address = server_socket.accept()
            console.print(f'[yellow]Connected with[yellow] {address}')
            get_messege(conn, address, session_token)

        except socket.error as err:
            print(err)
            continue



def get_messege(conn, address, session_token: str):
        current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        client_token = conn.recv(1024).decode()

        if client_token == session_token:
            console.print('[green]The token is correct, we are waiting for the message')
            response = 'True'
            conn.send(response.encode())

            message = conn.recv(1024).decode()
            

            console.print(f"[{(address[0])}] [{current_time}]: " + str(message.split()[0]))

            file = os.path.exists('history.txt')
            if not file:
                create_history_file()
            add_in_history(host, current_time, message)  
            logger.info(f'{address}: {message} {response}')             

        else:
            response = 'False'
            conn.send(response.encode())
            console.print('[red]The client entered the wrong session token. Connection closed')
            logger.info(f'{address} {response}') 
        conn.close()
        print('_____________________________')
    
        
if __name__ == '__main__':

    try:
        start = input('Start server? (enter/ Ctrl + C)')

    except KeyboardInterrupt:
        print('\nThe program is stopped !')
        sys.exit()

    host =  socket.gethostbyname(socket.gethostname())
    port = 5000
    password = (password_generation(True,False,False, 15))
    session_token = host + str(port) + str(password)

    print('Your host: ', host)
    print('Your port: ', port)
    print('Password: ', password)
    print('Session token: ', host, port , password)
    print('------------------------------')

    qr_token = qrcode.make(f'{host} {port} {password}')
    qr_token.save("session_token.png")
    qr_token = Image.open('session_token.png')
    qr_token.show() 

    server_socket = socket.socket(
    family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    await_connection(host, port, session_token)





