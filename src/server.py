import socket
import os
import sys
import time
from datetime import datetime
import toml



def add_in_history(host: str, current_time: str, message: str):

    time_and_messege = {}
    full_session_data = {}

    time_and_messege[current_time] = message
    full_session_data[host] = time_and_messege

    with open('history.toml', 'a') as file:
        toml.dump(full_session_data, file)




def connection_with_client(host, port):
    while True:

        try:
            print('Connection waiting...')


            conn, address = server_socket.accept()
            current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            print('connected with', address)

            get_messege(conn, address, current_time)

        except socket.error as err:
            print(err)
            pass



def get_messege(conn, address, current_time):
        try:
            message = conn.recv(1024).decode()

            

            print(f"[{(address[0])}] [{current_time}]: " + str(message))
            print('_____________________________')


            add_in_history(host, current_time, message)
        except socket.error as err:
            print(err)
            pass


if __name__ == '__main__':

    host =  socket.gethostbyname(socket.gethostname())
    port = 5000

    server_socket = socket.socket(
    family=socket.AF_INET, type=socket.SOCK_STREAM
    )
    server_socket.bind((host, port))
    server_socket.listen(2)
    # server_socket.setblocking(False)



    
    connection_with_client(host, port)

    # get_messege = get_messege(data[0], data[1], data[2])


    # print(get_messege)
