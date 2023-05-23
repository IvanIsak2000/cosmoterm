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


def check_token(conn: str, session_token: str) -> bool:
    get_client_token = conn.recv(1024).decode()
    if get_client_token == session_token:
        return True
    else:
        return False


def add_in_history(host: str, current_time: str, message: str):
    if not os.path.isfile('history.toml'):
        print('файла не было')
        create_history_file()
    time_and_messege = {}
    full_session_data = {}

    time_and_messege[current_time] = message
    full_session_data[host] = time_and_messege

    with open('history.toml', 'a') as file:
        toml.dump(full_session_data, file)    

def create_history_file():
    with open('history.toml', 'w') as file:
        file.write('Created!\n')


def await_connection(host: str, port: int, session_token: str):

    while True:
        try:
            console.print('[#9400D3]We are waiting for the connection...[#9400D3]')
            conn, address = server_socket.accept()
            console.print(f'[yellow]Connected with[yellow] {address}')
            send_response(conn, address, session_token)

        except socket.error as err:
            print(err)
            continue

def send_response(conn: str, address: str, session_token: str) :

    correcnt_token = check_token(conn, session_token)
    if correcnt_token :      
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

def get_message(conn, address)-> str:            
    message = conn.recv(1024).decode()
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    console.print(f"[{(address[0])}] [{current_time}]: " + str(message.split()[0]))
    add_in_history(address[0], current_time, message)  
    logger.info(f'{address}: {message} {True}')             

    conn.close()
    print('_____________________________')
    
        
if __name__ == '__main__':

    try:
        start = input('Start server? (enter/ Ctrl + C)')

    except KeyboardInterrupt:
        print('\nThe program is stopped !')
        sys.exit()
    logo = '''

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

    '''
    print(logo)
    
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





