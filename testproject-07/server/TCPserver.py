import socket  # 网络套接字
import time  # 时间戳
from threading import Thread  # 线程模块
from config import *

class TCP_server:
    def __init__(self):
        #  静态变量
        self.data = '已连接到服务器，请输入一个昵称'
        self.server = socket.socket()  # 默认使用TCP套接字

        self.HOSTNAME = socket.gethostname()
        self.IP = socket.gethostbyname(self.HOSTNAME)
        self.PORT = 8899

        #  调用绑定函数
        self.bind_tcp()

        #  客户端套接字，套接字对应的name
        self.clients = [ ]
        self.clients_name_ip = {}

        #  执行连接客户端方法
        self.get_client()

    #  绑定主机端口
    def bind_tcp(self):
        try:
            self.server.bind(('', self.PORT))  # 绑定端口
            self.server.listen()  # 最大监听数
        except Exception as error:
            print(f'绑定失败[{error}]')
        else:
            print(f'端口绑定成功，IP[{self.IP}],PORT[{self.PORT}],主机名[{self.HOSTNAME}]\n等待用户连接...')

    #  与客户端建立连接
    def get_client(self):
        while True:
            try:
                #  accept方法将返回两个值:套接字（client),地址（address),赋给相应变量
                client, address = self.server.accept()
            except Exception as error:
                print(f'与客户端建立连接错误[{error}]')
            else:
                #  将连接的用户套接字添加至列表
                self.clients.append(client)

            #  这里是第一次client向server发起请求时，服务端发送的消息
            client.send(self.data.encode())  # '已连接到服务器，请输入一个昵称'

            #  启动线程
            Thread(target=self.get_msg, args=(client, self.clients, self.clients_name_ip, address)).start()

    #  对客户端的消息处理
    def get_msg(self, client, clients, clients_name_ip, address):

        name = client.recv(1024).decode()
        clients_name_ip[ address ] = name
        recvinfo = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']\n' + f'欢迎{name}加入聊天室。'
        client.send(recvinfo.encode())

        #  开始循环监听消息
        while True:
            recvMSG = client.recv(1024).decode()
            time.sleep(0.1)
            for i in clients:
                i.send((address[ 0 ] + ':' + str(address[ 1 ]) + ' ' + str(f'[{clients_name_ip[ address ]}]') + ' ' + time.strftime("%H:%M:%S") + '\n' + recvMSG).encode())

    #  关闭套接字
    def close_client(self, client, address):
        self.clients_name_ip.pop(address)
        self.clients.remove(client)
        client.close()
        for g in self.clients:
            time.sleep(0.1)
            g.send(('[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']\n' + '[' + self.clients_name_ip[address ] + ']' + ' 已经离开').encode())
            self.clients_name_ip.pop(address)

if __name__ == '__main__':
    TCP_server()
