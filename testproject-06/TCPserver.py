import random
import socket  # 网络套接字
import time  # 时间戳
from threading import Thread  # 线程模块

class TCPserver:
    def __init__(self):
        self.clients = []
        self.client_name = {}
        self.bind()
        self.waite_connect()

    def bind(self):
        IP = '127.0.0.1'
        PORT = 8899
        self.server = socket.socket()
        self.server.bind((IP, PORT))
        self.server.listen()

    def waite_connect(self):
        while True:
            #  time.sleep(1)
            client_socket, address_info = self.server.accept()
            self.clients.append(client_socket)
            client_socket.send(('请输入一个昵称').encode())
            print(1)
            Thread(target=self.get_msg, args=(client_socket, address_info)).start()

    def get_msg(self, client_socket, address_info):
        name = client_socket.recv(1024).decode()
        self.client_name[address_info] = name
        while True:
            chat_data = client_socket.recv(1024).decode()
            if chat_data == 'quit':
                self.close_connect(client_socket, address_info)
                break
            for i in self.clients:
                i.send((self.client_name[address_info]+f':{chat_data}').encode())

    def close_connect(self, client_socket, address_info):
        client_socket.close()
        self.clients.remove(client_socket)
        self.client_name.pop(address_info)

if __name__ == '__main__':
    TCPserver()