import operator  # 用于列表的比较
from threading import Thread  # 线程模块
from config import *    # 部分功能模块

class TCP_server:
    def __init__(self):

        #  静态变量
        self.data = '已连接到服务器，请输入一个昵称'
        self.server = socket.socket()  # 默认使用TCP套接字

        #  调用绑定函数
        self.bindtcp()

        #  客户端套接字，套接字对应的name
        self.clients_socket = []
        self.clients_name_ip = {}
        self.local_user_list = []

        #  执行连接客户端方法
        self.getclient()

    #  绑定主机端口
    def bindtcp(self):
        """
        默认绑定8899端口
        :return:
        """
        try:
            self.server.bind(('', 8899))  # 绑定端口
            self.server.listen()  # 最大监听数
        except Exception as error:
            save_logs('run_error', error, '')
        else:
            save_logs('run_success', '', '')

    #  与客户端建立连接
    def getclient(self):
        """
        与客户端建立连接，accept方法是阻塞的，如果没有客户端连接则一直是阻塞状态
        当有客户端请求连接，将客户端的套接字信息储存至列表，然后启动一个接收消息（getmsg）的线程任务
        :return:
        """
        while True:
            try:
                #  accept方法将返回两个值:套接字（client),地址（address)
                client, address = self.server.accept()
            except Exception as error:
                save_logs('connect_error', error, '')
                continue
            else:
                #  将连接的客户端套接字添加至列表
                self.clients_socket.append(client)
                time.sleep(0.5)
                try:
                    #  这里是第一次client向server发起请求时，服务端发送的消息
                    client.send(self.data.encode())  # '已连接到服务器，请输入一个昵称'
                except Exception as error:
                    delete_info(self.clients_socket, self.clients_name_ip, address, client)
                    save_logs('send_error', error, '')
                else:
                    try:
                        #  启动线程
                        Thread(target=self.getmsg, args=(client, self.clients_socket, self.clients_name_ip, address)).start()
                    except Exception as error:
                        save_logs('thread_error', error, '')
                        delete_info(self.clients_socket, self.clients_name_ip, address, client)
                    else:
                        save_logs('connect_success', '', address)

    #  接收消息并处理
    def getmsg(self, client, clients_socket, clients_name_ip, address):
        """
        当此线程任务启动，将对客户端发送的消息进行接收并处理，在其中开启子线程任务发送用户列表信息
        :param client: 客户端套接字
        :param clients_socket: 存在有多个客户端套接字的列表
        :param clients_name_ip: 存在有多个客户端地址对应的昵称
        :param address: 客户端地址
        :return: Null
        """
        try:
            name = client.recv(1024).decode()
        except Exception as error:
            save_logs('close_client', error, address)
            delete_info(self.clients_socket, self.clients_name_ip, address, client)
        else:
            self.clients_name_ip[ address ] = name
            address_name = str(address) + ':' + str(name)
            save_logs('created_name', '', address_name)
            try:
                Thread(target=self.senduserlist, args=(clients_socket,)).start()
                recvinfo = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']\n' + f'欢迎{name}加入聊天室。'
                client.send(recvinfo.encode())
            except Exception as error:
                save_logs('close_client', error, address)
                delete_info(self.clients_socket, self.clients_name_ip, address, client)
            else:
                #  开始循环监听消息
                while True:
                    try:
                        recvMSG = client.recv(1024).decode()
                    except Exception as error:
                        save_logs('close_client', error, address)
                        self.closeclient(client, address)
                        break
                    else:
                        save_recvmsg(address, recvMSG)
                        if recvMSG == '#quit':
                            save_logs('leave_client', '', address)
                            self.closeclient(client, address)
                            break
                        #  广播消息（向所有在线用户转发消息）
                        self.broadcasting(clients_socket, address, clients_name_ip, recvMSG)

    #  发送用户列表
    def senduserlist(self, clients_socket, ):
        """
        当用户列表发生改变，就会执行一个对本地用户列表的判断，如果一致则不向客户端发送列表信息，否则发送信息
        发送完列表信息后，将改变的列表信息存储至本地
        :param clients_socket: 包含有用户套接字的列表
        :return: Null
        """
        while True:
            #  传入
            data, list_ = local_user_list(self.clients_name_ip)   #  传出用户列表字符串、用户列表
            time.sleep(1)
            #  分析
            if operator.eq(list_, self.local_user_list):
                continue
            else:
                #  转发信息
                for clients in clients_socket:
                    try:
                        clients.send(data.encode())
                    except Exception as error:
                        save_logs('send_userlist', error, clients)
                        break
                #  列表初始化、存入本地列表
                self.local_user_list = []
                self.local_user_list = list_

    #  转发消息
    def broadcasting(self, clients_socket, address, clients_name_ip, data):
        """
        将消息转发至所有在线的客户端
        :param clients_socket: 包含所有在线的客户端套接字
        :param address: 客户端地址
        :param clients_name_ip: 包含所有在线的客户端地址与对应的昵称
        :param data: 转发信息
        :return: Null
        """
        for i in clients_socket:
            time.sleep(0.1)
            try:
                i.send((address[ 0 ] + ':' + str(address[ 1 ]) + ' ' + str(
                    f'[{clients_name_ip[ address ]}]') + ' ' + time.strftime("%H:%M:%S") + '\n' + data).encode())
            except Exception as error:
                save_logs('send_error', error, '')

    #  关闭套接字
    def closeclient(self, client, address):
        """
        如果在程序执行中，客户端或者是服务端一方由某种操作断开连接，为了防止后续操作出错将对断开的客户端进行断开tcp连接并从客户端套接字列表中
        删除信息，同时删除客户端地址对应的昵称
        :param client:
        :param address:
        :return:
        """
        delete_info(self.clients_socket, self.clients_name_ip, address, client)

if __name__ == '__main__':
    TCP_server()
