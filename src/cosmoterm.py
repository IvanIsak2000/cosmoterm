import socket
import os
import sys
from datetime import datetime
import toml


def add_in_history(host: str, current_time: str, message: str):

    time_and_messege = {}
    full_session_data = {}

    time_and_messege[current_time] = message
    full_session_data[host] = time_and_messege

    with open('history.toml', 'a') as file:
        toml.dump(full_session_data, file)


def get_your_host_port() -> list:
    host = socket.gethostname()
    your_ip = socket.gethostbyname(host)
    print('Your IP: ', your_ip)
    port = str(
        input('Enter a your server port (default 5000 [press enter]): '))

    if port == '':
        port = 5000

    else:
        port = int(port)

    return your_ip, port


def get_message(host: str, port: str):

    print('To receive a message, your friend must enter your IP into the program')
    print('We are waiting for messages...')

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()

    os.system(f'{clear_messege}')
    message = conn.recv(1024).decode()
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    print(f"[{(address[0])}] [{current_time}]: " + str(message))
    conn.close()

    add_in_history(host, current_time, message)


def get_server_host_port() -> list:

    logo = """
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


    """
    print(logo)

    host = str(input('Enter  a friend IP: '))
    port = str(input('Enter a friend port (default 5000 [press enter]): '))

    if port == '':
        port = 5000

    else:
        port = int(port)

    return host, port


def connection_to_server_part(host: str, port: str) -> str:
    try:
        client_socket = socket.socket()
        client_socket.connect((host, port))
        print(f'Your friend with IP {host} online!')
        message = input("Enter your message: ")
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        client_socket.close()

        current_time = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        print('Message sent successfully!')

        add_in_history(host, current_time, message)

    except Exception as err:
        print(err)


if __name__ == '__main__':

    if os.name == 'nt':
        clear_messege = 'cls'

    else:
        clear_messege = 'clear'

    try:
        move = sys.argv[1]

        if move == '--r':
            your_host_port = get_your_host_port()
            get_message(your_host_port[0], your_host_port[1])

        elif move == '--s':
            server_host_port = get_server_host_port()
            connection_to_server_part(server_host_port[0], server_host_port[1])

        else:
            print('Fill in correctly: main.py <command (--r or --s)>')

    except Exception as err:
        print(err)
