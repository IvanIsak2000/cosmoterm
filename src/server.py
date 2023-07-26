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

logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


class Server:

    def __init__(self, host: str, port: int, password: int):
        self.host = host
        self.port = port
        self.password = password

        server_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM)

        try:
            server_socket.bind((host_, port_))

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

    def password_is_valid(self) -> bool:
        get_client_password = self.conn.recv(1024).decode()
        return get_client_password == self.password

    def add_in_history(self) -> None:
        if not os.path.isfile('history.toml'):
            self.create_history_file()

        time_and_messege = {}
        full_session_data = {}

        time_and_message = {self.current_time: self.message}
        full_session_data = {self.host: time_and_message}

        with open('history.toml', 'a') as file:
            toml.dump(full_session_data, file)

    def create_history_file(self) -> None:
        with open('history.toml', 'w') as file:
            file.write('Created!\n')

    def await_connection(self) -> None:
        while True:
            try:
                console.print(
                    '\n[#9400D3]We are waiting for the connection...[#9400D3]')
                conn, address = self.server_socket.accept()
                self.conn = conn
                self.address = address
                console.print(f'[yellow]Connected with[yellow] {self.address}')
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

        if self.password_is_valid():
            response = 'True'
            self.conn.send(response.encode())
            console.print(
                '[green]The token is correct, we are waiting for the message')
            self.get_message()

        else:
            response = 'False'
            self.conn.send(response.encode())
            console.print(
                "[red]The client entered an invalid session password or did not enter a password. Connection closed ")
            logger.info(f'{self.address}: {response}')
            self.conn.close()

    def get_message(self) -> None:
        message = self.conn.recv(1024).decode()
        self.message = message
        current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.current_time = current_time
        console.print(
            f"[{(self.address)}] [{self.current_time}]: " + str(self.message.split()[0]))
        self.add_in_history()
        logger.info(f'{self.address}: {message} {True}')

        self.conn.close()
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
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        help='set port for connection',
        default=5000)
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

    server = Server(host_, port_, password)
    server.await_connection()
