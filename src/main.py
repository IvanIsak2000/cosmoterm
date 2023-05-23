import os
import sys
from  genp import password_generation
import socket
from datetime import datetime
import logging
                                                                              
from  winreg import * 
from rich.console import Console

console = Console(highlight=False)
logging.basicConfig(filename='client.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


def connection_to_server_part(host: str, port: str) -> str:
    global client_socket
    try:
        client_socket = socket.socket()
        client_socket.connect((host, port))
        console.print(f'[yellow]Your friend with IP {host} online!')

        correct_response = send_and_get_response()

        if correct_response:
            console.print('[green]Connection approved')  
            message = input("Enter your message: ")                      
            send(message)

            current_time = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            console.print('[green]Message sent successfully!')
            logger.info(f'{host}: {message}')

        else:
            console.print('[red]Wrong token!')
            

        client_socket.close()
        
    except KeyboardInterrupt:
        sys.exit()

    except Exception as err:
        print(err)
            

def send_and_get_response() -> bool:
    client_socket.send(token.encode())
    response = client_socket.recv(1024).decode()
    if response == "True":
        return True
    else:
        return False

def send(message: str):
    client_socket.send(message.encode())

    


if __name__ =='__main__':

    try:
        action = sys.argv


        if action[1] =='--set':
            key_my = OpenKey(HKEY_CURRENT_USER, 
                            r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 
                            0, KEY_ALL_ACCESS)

            SetValueEx(key_my, 'server.py', 0, REG_SZ, r'C:\GITHUB\COSMOTERM_V0\cosmoterm\src\server.py')

            CloseKey(key_my)

            print('Done!\nserver.py set in startup!')
            for_exit = input()



        elif action[1] == '--unset':
            #удалить сервер из автозагрузок
            pass


        elif action[1] == '--send':


            token = str(action[2] + action[3] + action[4])
            connection_to_server_part(str(action[2]), int(action[3]))

        else:
            print('Error when entering a command!\nAvailable commands:\npython main.py --set (configures the server.py in a startup, so that the server is restarted when the PC is turned on)\npython main.py --send <host> <port> <password>')
            input()

    except IndexError:
        print('The correct entry is:\npython main.py --set \npython main.pt --send <host> <port> <password>')
        input()

    except Exception as err:
        print(err)
        input()
