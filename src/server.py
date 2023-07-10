#!/usr/bin/python3

import socket
import os
import sys
import argparse
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


def password_is_valid(conn: socket.socket, password: str) -> bool:
    print(f'server password {password}')
    get_client_password = conn.recv(1024).decode()
    return get_client_password == password


def add_in_history(host: str, current_time: str, message: str) -> None:
    if not os.path.isfile('history.toml'):
        create_history_file()
        print('There was no file - successfully created.')
        
    time_and_messege = {}
    full_session_data = {} 
    
    time_and_message = {current_time: message}
    full_session_data = {host: time_and_message}
    
    with open('history.toml', 'a') as file:
        toml.dump(full_session_data, file)


def create_history_file() -> None:
    with open('history.toml', 'w') as file:
        file.write('Created!\n')


def await_connection(host_: str, port_: int) -> None: 
    server_socket = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM)

    server_socket.bind((host_, port_))
    server_socket.listen(2)

    while True:
        try:
            console.print('\n[#9400D3]We are waiting for the connection...[#9400D3]')
            conn, address = server_socket.accept()
            console.print(f'[yellow]Connected with[yellow] {address}')
            send_response(conn, address, password)

        except socket.error as err:
            print(err)

def send_response(conn: socket.socket, address: tuple[str, int], password: str) -> None:
   
    if password_is_valid(conn, password):   
        response = 'True'   
        conn.send(response.encode())
        console.print('[green]The token is correct, we are waiting for the message')  
        get_message(conn, address)

    else:
        response = 'False'
        conn.send(response.encode())
        console.print("[red]The client entered an invalid session password or did not enter a password. Connection closed ")
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
    


if __name__ == '__main__':

    print("""

       :BG:
      ?@@@&7                                                                                                               :Y
     J@@@@@@?                                                                                                              !&
    :@@&GG&@&.           .!JJJJJ7:         .7JJJJJ7:         :?JJJJJ7.      ?^ !?JJYJ^  .!?JJYJ~          ^?JJJJJ~       7?G&J?J~       ^?JJJJJ!.       ~7 ^?JY~   ~? ^?JJYY!   ~?JJYY7.
    J@@^  ~@@!         .PP~.   .^5B:     .GP^.   .^5G.      GP:    .!B7     ##J^    :GG75^    :P#.      !B?:    .7BJ       7&.        ^BY:    .!G5      5&57.      Y&Y~.   .J#!5~.   .?&^
    ?@@BJY#@@~        .&7         ?P    :&7         !&:    ~@        .:     #B        &#        #5     Y#.         GG      !&        7&.         YB     Y&.        Y&.       5@.       J&
    !@@@@@@@@:        GP                B5           Y#     GG~.            #Y        B5        PB    :@:           &!     !&       .&!          .&?    YB         Y#        ?&        !&
    :@@@@@@@&         &7                &~           ~&.     :7JYYYJ7.      #Y        BP        PG    7&            B5     !&       ^@Y?JJJJJJJJJ?5~    YB         Y#        ?&        !&
  .?.&@@@@@@G:5.      BP                #Y           J#            .~B5     #Y        BP        PG    ^@.           &7     !&       .&^                 YB         Y#        ?&        !&
  &@^G@@@@@@J7@B      :&!         !P    ^&~         ^&^    ^.        .@:    #Y        BP        PG     PB          PB      !&        ?#.          .     YB         Y#        ?&        !&
  #&^!#&&&#B:!&Y       :B5^     :Y#^     :BY:     :YB^     7#!.     ^GP     #Y        BP        GB      ?B7.    .~G5       .&?        !B?.     .?B!     5#         Y#        ?&        !&
  .   ^JJJ?.             :?YJJJYJ^         ^?YJJJY?^        .7JJJJJJ?:      J~        ?!        7?        !JYJJYJ7.         .?YYY.      ~JYJJJYJ~       !J         ~J        ^Y        :5
      .Y .5
      ~P .B.
       ~YY.    
    """)

    host_ = socket.gethostbyname(socket.gethostname())

    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port', type=int, help='set port for connection', default=5000)
    arg = parser.parse_args()

    port_ = arg.port

    password = password_generation(True, False, False, 15)

    console.print(f"""
[green]Your host: {host_}
Your port: {port_}
Password: {password}
Full session data (token): {host_} {port_} {password}
-----------------------------------------""")

    qr_token = qrcode.make(f'{host_} {port_} {password}')
    qr_token.save("session_token.png")
    qr_token = Image.open('session_token.png')
    qr_token.show() 

    await_connection(host_, port_)
