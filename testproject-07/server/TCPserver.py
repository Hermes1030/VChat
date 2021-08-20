import socket  # 网络套接字
import time  # 时间戳
import operator
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
        self.clients_socket = []
        self.clients_name_ip = {}
        self.user_list = []
        self.user_num = 0

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
            print(f'端口绑定成功，地址：[{self.IP}:{self.PORT}],主机名[{self.HOSTNAME}]\n等待用户连接...')

    #  与客户端建立连接
    def get_client(self):
        while True:
            try:
                #  accept方法将返回两个值:套接字（client),地址（address),赋给相应变量
                client, address = self.server.accept()
            except Exception as error:
                print(f'[{time.strftime("%X")} 错误]：未能与客户端建立连接{error}')
                continue
            else:
                #  将连接的用户套接字添加至列表
                self.clients_socket.append(client)
                time.sleep(0.5)
                try:
                    #  这里是第一次client向server发起请求时，服务端发送的消息
                    client.send(self.data.encode())  # '已连接到服务器，请输入一个昵称'
                except Exception as error:
                    delete_info(self.clients_socket, self.clients_name_ip, address, client)
                    print(f'[{time.strftime("%X")} 错误]：data发送失败{error}')
                else:
                    try:
                        #  启动线程
                        Thread(target=self.get_msg, args=(client, self.clients_socket, self.clients_name_ip, address)).start()
                    except Exception as error:
                        print(f'[{time.strftime("%X")} 错误]：get_msg线程任务启动失败{error}')
                        delete_info(self.clients_socket, self.clients_name_ip, address, client)
                    else:
                        print(f'[{time.strftime("%X")} 通知]：{address}连接成功，问候信息发送成功，消息接收线程启动成功。\n'
                              f'>>>now clients_socket list:{self.clients_socket},'
                              f'address list:{address},'
                              f'clients_name_ip list:{self.clients_name_ip}')

    #  对客户端的消息处理
    def get_msg(self, client, clients_socket, clients_name_ip, address):
        try:
            name = client.recv(1024).decode()
        except Exception as error:
            print(f'[{time.strftime("%X")} 提示]：与客户端[{address}]断开连接{error}')
            delete_info(self.clients_socket, self.clients_name_ip, address, client)
        else:
            self.clients_name_ip[ address ] = name
            print(f'[{time.strftime("%X")} 通知]：客户端[{address}]创建了一个昵称：{name}')
            Thread(target=self.sendUSERnum, args=(client, clients_socket)).start()
            try:
                recvinfo = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']\n' + f'欢迎{name}加入聊天室。'
                client.send(recvinfo.encode())
            except Exception as error:
                print(f'[{time.strftime("%X")} 错误]：与客户端[{address}]断开连接{error}')
                delete_info(self.clients_socket, self.clients_name_ip, address, client)
            else:
                #  开始循环监听消息
                while True:
                    try:
                        recvMSG = client.recv(1024).decode()
                    except Exception:
                        print(f'[{time.strftime("%X")} 错误]：与客户端[{address}]断开连接')
                        self.close_client(client, address)
                        break
                    else:
                        if recvMSG == '#quit':
                            print(f'[{time.strftime("%X")} 提示]：客户端[{address}]下线')
                            self.close_client(client, address)
                            break
                        for i in clients_socket:
                            time.sleep(0.1)
                            try:
                                i.send((address[ 0 ] + ':' + str(address[ 1 ]) + ' ' + str(f'[{clients_name_ip[ address ]}]') + ' ' + time.strftime("%H:%M:%S") + '\n' + recvMSG).encode())
                            except Exception as error:
                                print(f'[{time.strftime("%H:%M:%S")} 错误]：消息发送失败[{error}]来自套接字：{i}')

    def sendUSERnum(self, client, clients_socket):
        Thread(target=self.sendUSERlist, args=(clients_socket,)).start()
        while True:
            if self.user_num != len(clients_socket):
                try:
                    data = '在线人数' + str(len(clients_socket))
                    time.sleep(1)
                    client.send(data.encode())
                    self.user_num = len(clients_socket)
                except Exception:
                    break

    def sendUSERlist(self, clients_socket,):
        while True:
            #  传入
            data, list_ = user_list(self.clients_name_ip)
            time.sleep(1)
            #  分析
            if operator.eq(list_, self.user_list):
                continue
            else:
                #  传输信息区
                for clients in clients_socket:
                    try:
                        clients.send(data.encode())
                    except Exception as error:
                        print(f'[{time.strftime("%H:%M:%S")} 错误]：用户列表发送失败[{error}]来自套接字：{clients}')
                        break
                self.user_list = list_

    #  关闭套接字
    def close_client(self, client, address):
        delete_info(self.clients_socket, self.clients_name_ip, address, client)
        if self.user_num >= 1:
            self.user_num = self.user_num - 1

if __name__ == '__main__':
    TCP_server()
