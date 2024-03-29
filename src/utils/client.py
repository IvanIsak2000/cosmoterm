import os
import sys
import argparse
import socket
from datetime import datetime
from rich.console import Console

from utils.logger import logger
from utils.model import add_target
from utils.model import get_targets

class Client:
    """В идеале должен выводить окно терминала и спрашивать кому отправить сообщения.
    Первоначально будет предлагаться добпаивть ip+host друзей, и генерация для них уникального ключа вместо ввода сокета.
    """

    def __init__(self):
        console = Console(highlight=False)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = client_socket 
 

    def add_new_target(self):
        """Выводиться когда список целей пуст и предлагает добавить новую цель посредством ввода имена цели, хоста, порта."""
        """Activate where no one targets for sennging is not exist in local databae"""

        self.console.print('[red]Sorry, but no one targets not exist! Please make new targer')
        new_target_name = input('Write custom target name (likely: Jonn):')
        new_target_host = input('Write target host (likely:xxx.xxx.xx.xx):')
        new_target_port = input('Write target port (likely: xxxx):')
        add_target(new_target_name, new_target_host, new_target_port)


    def choose_target(self) -> dict:
        """Get local saved targets and get user answer to choose target"""
        targets = get_targets()
        print('\n'.join([str(t) for t in targets]))
        target_id = int(input('Please target for sending by id:\n'))
        target = targets[target_id]
        return {'host':target.host, 'port': target.port}
    

    def start_client_part(self, target) -> None:
        """Get socket to send.
        Sending: Step 1"""

        targets = get_targets()
        if targets is None:
            self.add_new_target()  

        chosen_target = self.choose_target()
        self.send_message(chosen_target)
        host = target.host
        self.client_socket.connect((host, port))  
        try:
            self.console.print(f'[yellow]Your friend with IP {self.host} online!')
            correct_response = self.send_key_to_check_permission_to_sending()

            if correct_response:
                logger.info('Connected')
                self.console.print('[green]Connection approved') 
                if self.message == None: 
                    self.message = input("Enter your message: ")  
                self.send_message()
                current_time = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                self.console.print('[green]Message sent successfully!')
                logger.info(f'Connected: {self.host}: {self.message}')

            else:
                self.console.print('[red]Wrong token!')
                logger.error('Wrong token')

            self.client_socket.close()
            
        except KeyboardInterrupt:
            logger.info('User closed program')
            sys.exit()

        except Exception as e:
           logger.exception(e)
                

    def send_key_to_check_permission_to_sending(self) -> bool:
        """Get a key, send permisson key to server and return that server response is True to start sending
        Sending: Step 2"""

        self.client_socket.send(self.key.encode())
        response = self.client_socket.recv(1024).decode()
        return response == 'True'
    

    def send_message(self) -> None:
        """Sending: Step 3"""
        self.client_socket.send(self.message.encode())

# для дебажнинга 
# c = Client()
# c.main()