import os
import sys
from  genp import password_generation
import socket
from datetime import datetime
import qrcode
from PIL import Image                                                                                
from  winreg import * 
# from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx

# with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
#     Downloads = QueryValueEx(key, r'{FDD39AD0-238F-46AF-ADB4-6C85480369C7}')[0]

#     print(Downloads)


#1. Надо полчуить путь к папке автозапуска

#2. чел пишет --set и прога по пути устанавливает server.py в автозагрузки

#3. при каждом запуске винды включается и сервер, имеющий лог файл

#4. когда чел хочет отправить сообщения пишет --send

#5. можно сделать генераци IP, host-a и какого нибудь ключа рандомно сгенерировано и все данные в QR а уже этот QR передать другу

move = sys.argv
print(move)






host =  socket.gethostbyname(socket.gethostname())
port = 5000
# token = password_generation(True, 0, False, 6)

token = 602762

if move[1] =='--set':
    key_my = OpenKey(HKEY_CURRENT_USER, 
                    r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 
                    0, KEY_ALL_ACCESS)

    SetValueEx(key_my, 'script', 0, REG_SZ, r'pri.py')

    CloseKey(key_my)


    # def server():
    #     #создание QR изображения из IP, host, secret(случайно сгенерированого в одной сесии токена)
    #     pass 

    # path ='путь к автозагрузкам'

    # # with open (path, 'w') as server_file:
    # #     server_file.write(server())


elif move[1] == '--unset':
    #удалить сервер из автозагрузок
    pass



elif move[1] == '--get':



    #если чел захочет самостоятельно включть


    '''
    созданеи автономног сервера через while дял принятие соединения
    '''



    img = qrcode.make(f'host:{host}\nport:{port}\ntoken:{token}')

    img.save("file.png")
    img = Image.open('file.png')
    img.show()
    z = input()
        




        
elif move[1] == '--send':

    #если чел захочет сам
    print(host, port )
    # if move[2] == host and int(move[3]) ==port and int(move[4]) == token:
    #     print('conn')


    def connection_to_server_part(host: str, port: str) -> str:
        try:
            client_socket = socket.socket()
            client_socket.connect((host, port))
            print(f'Your friend with IP {host} online!')
            message = input("Enter your message: ")
            client_socket.send(message.encode())
            # data = client_socket.recv(1024).decode()
            client_socket.close()

            current_time = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

            print('Message sent successfully!')



        except Exception as err:
            print(err)
    
    connection_to_server_part('192.168.0.139', 5000)
    #чел сканирует QR получает IP, host, secret
    #отправляет
   
