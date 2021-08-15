import random
import socket  # 网络套接字
import time  # 时间戳
from threading import Thread  # 线程模块

class TCP_server:
    def __init__(self):

        #  输出主机名、IP，并显示状态
        HOSTNAME = socket.gethostname()
        IP = socket.gethostbyname(HOSTNAME)
        PORT = 8899
        #  调用绑定函数
        self.bind_tcp(PORT)

        #  将系统信息写入日志文件
        server_info = f'{time.strftime("%Y-%m-%d %H:%M:%S")}>>>服务器运行，当前主机名 {HOSTNAME} 内网IP为 {IP} 默认端口 {PORT}。\n{time.strftime("%Y-%m-%d %H:%M:%S")}>>>等待用户连接... '
        self.write_logs(server_info, '')

        #  客户端套接字，套接字对应的name
        self.clients = [ ]
        self.clients_name_ip = {}
        #  执行连接客户端方法
        self.get_client()

    #  绑定主机端口
    def bind_tcp(self, PORT):
        self.data = '已连接到服务器，请输入一个昵称'
        self.server = socket.socket()  # 默认使用TCP套接字
        try:
            self.server.bind(('', PORT))  # 绑定端口
            self.server.listen()  # 最大监听数
        except Exception as error:
            server_info = f'\n{time.strftime("%Y-%m-%d %H:%M:%S")}>>>绑定失败...|错误描述：' + str(error)
            self.write_logs(server_info, '')

    #  与客户端建立连接
    def get_client(self):
        while True:
            #  accept方法将返回两个值:套接字（client),地址（address),赋给相应变量
            client, address = self.server.accept()
            server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']   客户端 ' + str(address[ 0 ]) + ':' + str(
                address[ 1 ]) + ' 连接成功'
            self.write_logs(server_info, '')
            #  将连接的用户套接字添加至列表
            self.clients.append(client)
            '''
            消息的发出与接收需要解码
            send encode
            recv decode
            '''
            #  这里是第一次client向server发起请求时，服务端发送的消息
            try:
                client.send(self.data.encode())  # '已连接到服务器，请输入一个昵称'
            except Exception as error:
                server_info = '[系统消息' + ' ' + time.strftime(
                    "%H:%M:%S") + f']   消息发送失败，与客户端的连接已断开。  |错误描述:{error}'
                self.write_logs(server_info, '')
                self.clients.remove(client)
                client.close()
            try:
                #  启动多个线程
                Thread(target=self.get_msg, args=(client, self.clients, self.clients_name_ip, address)).start()
            except Exception as error:
                server_info = '[系统消息' + ' ' + time.strftime(
                    "%H:%M:%S") + f']   线程未能启动，并与客户端的连接已断开。  |错误描述:{error}'
                self.write_logs(server_info, '')
                self.clients.remove(client)
                client.close()
    #  对客户端的消息处理
    def get_msg(self, client, clients, clients_name_ip, address):
        try:
            name = client.recv(1024).decode()
            if name[ 0 ] != '#':
                clients_name_ip[ address ] = name
                recvinfo = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']\n' + f'欢迎{name}加入聊天室。'
                client.send(recvinfo.encode())

                server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']   客户端 ' + str(address[ 0 ]) + ':' + str(
                    address[ 1 ]) + f' 创建用户名为：[{name}]'
                self.write_logs(server_info, '')
            else:
                uname = '未创建用户名'
                clients_name_ip[ address ] = uname + str(len(clients))
                recvinfo = '[系统消息' + ' ' + time.strftime("%X") + ']\n' + f'您输入的昵称违规\n{address}加入聊天室。'
                client.send(recvinfo.encode())

                server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']   客户端 ' + str(address[ 0 ]) + ':' + str(
                    address[ 1 ]) + f' 因创建用户名违规，用户名更改为：[未命名用户{len(clients)}]'
                self.write_logs(server_info, '')
        except Exception as error:
            server_info = '[系统消息' + ' ' + time.strftime(
                "%H:%M:%S") + f']   消息发送失败，未收到对方创建的昵称，与客户端的连接已断开。   |错误描述:{error}'
            self.write_logs(server_info, '')
            self.clients.remove(client)
        else:
            Send_Users = Thread(target=self.send_users_data, args=(self.clients, self.clients_name_ip))
            Send_Users.start()
            Send_Users.join(1)
        # print(clients_name_ip)
        #  循环监听消息
        while True:
            try:
                recvMSG = client.recv(1024).decode()
            except Exception as error:
                server_info = '[系统消息' + ' ' + time.strftime(
                    "%H:%M:%S") + f']   消息接收失败，与客户端 {address[ 0 ]}:{address[ 1 ]} 的连接已断开。   |错误描述:{error}'
                self.write_logs(server_info, '')
                self.close_client(client, address)
                break
            #  聊天记录写入到文件
            try:
                info = '[系统消息' + ' ' + time.strftime(
                    "%H:%M:%S") + ']   ' + f'客户端 {address[ 0 ]}:{address[ 1 ]} 发送了一条消息。   |key:{self.makekey()}'
                self.write_logs('', info)
                self.write_messages(info, address, recvMSG)
            except Exception as error:
                server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + f']   数据写入失败    |错误描述:{error}'
                self.write_logs(server_info, '')
            #  指令集功能区
            #  如果用户发送 ‘#QUIT’
            if recvMSG.upper() == '#QUIT':
                self.close_client(client, address)
                if address in clients_name_ip:
                    self.clients_name_ip.pop(address)
                break
            #  如果用户发送 ’#SHOW USERS
            if recvMSG.upper() == '#SHOW USERS':
                client.send(('[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']\n' + str(clients_name_ip)).encode())
            else:
                for i in clients:
                    try:
                        i.send((address[ 0 ] + ':' + str(address[ 1 ]) + ' ' + str(f'[{clients_name_ip[ address ]}]') + ' ' + time.strftime("%H:%M:%S") + '\n' + recvMSG).encode())
                    except Exception as error:
                        self.clients.remove(client)
    #  关闭套接字
    def close_client(self, client, address):
        if client not in self.clients:
            server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + f']   ' + f'{client} not in clients'
            self.write_logs(server_info, '')
            if address in self.clients_name_ip:
                self.clients_name_ip.pop(address)
        else:
            self.clients.remove(client)
            client.close()

            server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']   ' + '[' + self.clients_name_ip[address ] + ']' + ' 已经离开'
            self.write_logs(server_info, '')
            for g in self.clients:
                g.send(('[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']\n' + '[' + self.clients_name_ip[address ] + ']' + ' 已经离开').encode())
            self.clients_name_ip.pop(address)

    #  实时同步在线人数
    def send_users_data(self, clients, clients_name_ip):
        while True:
            time.sleep(3)
            for i in clients:
                user = '|'
                for useradd in clients_name_ip.keys():
                    user = user + str(clients_name_ip[ useradd ]) + 'IP:' + str(useradd)[ 2:-9: ] + ':' + str(useradd)[-6:-1: ] + '|'
                try:
                    i.send(f'userdata:{len(clients_name_ip)}{user}'.encode())
                except Exception as error:
                    server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']   ' + f'用户信息消息发送失败    |错误描述：{error}'
                    self.write_logs(server_info, '')
                    break

    #  保存日志
    def write_logs(self, data, info):
        if data != '':
            print(data)
        try:
            file = open('logs', mode='a+', encoding='utf8', )
            if data == '':
                file.write(info + '\n')
            if info == '':
                file.write(data + '\n')
            file.close()
        except Exception as error:
            print('[系统消息' + ' ' + time.strftime("%Y-%m-%d %H:%M:%S") + ']   ' + f'日志写入失败    |错误描述:{error}')

    #  保存聊天记录
    def write_messages(self, info, address, text):
        i1 = ''
        for i in info[ ::-1 ]:
            if i == ':':
                break
            i1 += i
        i2 = '[' + i1[ ::-1 ] + ']' + address[ 0 ] + ':' + str(address[ 1 ]) + ':' + text
        file = open('messages', mode='a+', encoding='utf8')
        file.write(i2 + '\n')
        file.close()

    #  生成编码
    def makekey(self):
        abc = [ 'a', 'b', 'c', 'e', 'f', 'A', 'B', 'C', 'E', 'F' ]
        pd = random.randint(1111111111111111111, 9999999999999999999)  # len:19
        pdd_ = [ ]
        for i in str(pd):
            pdd_.append(str(i))
        for g in str(pd):
            pdd_[ int(g) ] = abc[ int(g) ]
        key = ''
        for i in pdd_:
            key += i
        return key


if __name__ == '__main__':
    TCP_server()
