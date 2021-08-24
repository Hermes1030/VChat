import time
import random
import datetime
import socket

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname(HOSTNAME)
PORT = 8899

#  生成编码
def make_key():
    '''
    生成一个随机编码
    :param self:
    :return: key
    '''
    abc = [ 'g', 'z', 'q', 'a', 'f', 'A', 'B', 'C', 'E', 'F' ]
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

#  从套接字列表中删除客户端相关信息
def delete_info(clients_socket, clients_name_ip, address, client):
    '''
    删除存储的套接字信息
    :param clients_socket: list
    :param clients_name_ip: list
    :param address: tuple
    :param client: socket
    :return: clients_socket, clients_name_ip :list
    '''
    if client in clients_socket:
        clients_socket.remove(client)
    if address in clients_name_ip:
        clients_name_ip.pop(address)
    try:
        client.close()
    except Exception as error:
        print(f'套接字关闭失败[{error}]')

    return clients_socket, clients_name_ip

#  用户列表处理
def local_user_list(userlist):
    """
    将传入的用户列表对其进行处理，先是转换成字符串以便发送至客户端，然后生成一个用户列表（list_）
    :param userlist: 传入的用户列表
    :return:
    """
    data = '列表用户|'
    sa = ''
    for user_name in userlist.keys():
        data += str(userlist[ user_name ]) + '[' + str(user_name)[ 2:-1: ] + ']' + '|'
    for i in data:
        if i == "'" or i == ",":
            continue
        elif i == ' ':
            i = ':'
            sa += i
        else:
            sa += i
    s = ''
    list_ = [ ]
    # type(sa):str
    # sa结果：列表用户|user1[127.0.0.1:49768]|user2[127.0.0.1:49769]|
    try:
        for i in data[ 4:: ]:
            if i == '|':
                continue
            elif i == ']':
                i = ']\n'
                s += i
                list_.append(s[ :-1: ])
                s = ''
            else:
                s += i
    except Exception:
        pass
    #  list_ = [
    #           user1[127.0.0.1:49768],
    #           user2[127.0.0.1:49769],
    #          ]
    return sa, list_

#  保存聊天记录
def save_recvmsg(address, data):
    key = make_key()
    text = f'[{key}]:{data}'
    try:
        recv_file = open(f'{datetime.datetime.now().strftime("%Y-%m-%d")}.recv', mode='a+', )
        recv_file.write(text + '\n')
        recv_file.close()
        save_logs('saverecvmsg_info', key, address)
    except Exception as error:
        save_logs('saverecvmsg_error', error, '')


#  保存日志
def save_logs(flag, error, address):
    data = '无数据'
    if flag == 'run_success':
        data = f'[{time.strftime("%X")} 信息] 端口绑定成功，地址：[{IP}:{PORT}],主机名[{HOSTNAME}]\n等待用户连接...'
    if flag == 'run_error':
        data = f'[{time.strftime("%X")} 错误] 端口绑定失败{error}'
    elif flag == 'connect_success':
        data = f'[{time.strftime("%X")} 成功]：{address}连接成功，问候信息发送成功，消息接收线程启动成功。'
    elif flag == 'connect_error':
        data = f'[{time.strftime("%X")} 错误] 未能与客户端建立连接{error}'
    elif flag == 'send_error':
        data = f'[{time.strftime("%X")} 失败]：消息发送失败{error}'
    elif flag == 'thread_error':
        data = f'[{time.strftime("%X")} 错误]：getmsg线程任务启动失败{error}'
    elif flag == 'close_client':
        data = f'[{time.strftime("%X")} 错误]：与客户端[{address}]断开连接{error}'
    elif flag == 'created_name':
        data = f'[{time.strftime("%X")} 信息]：客户端[{address}]加入'
    elif flag == 'leave_client':
        data = f'[{time.strftime("%X")} 信息]：客户端[{address}]下线'
    elif flag == 'send_userslist':
        data = f'[{time.strftime("%X")} 失败]：用户列表发送失败[{error}]来自套接字：{address}'
    elif flag == 'saverecvmsg_error':
        data = f'[{time.strftime("%X")} 失败]：聊天信息写入失败{error}'
    elif flag == 'saverecvmsg_info':
        data = f'[{time.strftime("%X")} 信息]：用户{address}发送了一条消息 {error}'
    print(data)
    try:
        log_file = open(f'{datetime.datetime.now().strftime("%Y-%m-%d")}.log', mode='a+', )
        log_file.write(data + '\n')
        log_file.close()
    except Exception:
        pass


'''
消息的发出与接收需要解码
send encode
recv decode
'''
