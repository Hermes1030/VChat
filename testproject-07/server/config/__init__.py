import random

'''
消息的发出与接收需要解码
send encode
recv decode
'''

#  生成编码
def make_key(self):
    '''
    生成一个随机编码
    :param self:
    :return: key
    '''
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

def user_list(userlist):

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
    list_ = []
    # 列表用户|user1[127.0.0.1:49768]|user2[127.0.0.1:49769]|
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
#  保存日志
