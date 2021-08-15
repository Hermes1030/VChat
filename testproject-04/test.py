# # i = ('1234', 6666)
# # print(i)
# # print('this is i[0]:' + i[0])
# # # print('this is i[1]:' + str(i[1])
# # print(str(i[1]))
# # import random
# # name_list = {}
# # # {('127.0.0.1', 62795): '高'}
# #
# # # userdata:1| 高IP:127.0.0.1:49606|
# # for i in range(1, 5):
# #     a = random.randint(0, 254)
# #     b = random.randint(0, 254)
# #     c = random.randint(0, 254)
# #     d = random.randint(0, 254)
# #     e = random.randint(6667, 65534)
# #     ip = f'{a}.{b}.{c}.{d}', e
# #     name = f'用户{i}'
# #     name_list[ip] = name
# # i = ' '
# # # print(len(name_list))
# # for I in name_list.keys():
# #     # print(I)
# #     # print(name_list[I], 'IP:'+str(I)[2:-9:] + ':' + str(I)[-6:-1:])
# #     i = i + '\n' + str(name_list[I]) + str(I)
# #
# # print('i:',i)
#
#
#
# #  userdata:1| 高IP:127.0.0.1:49606|高IP:127.0.0.1:49605|高IP:127.0.0.1:49604|高IP:127.0.0.1:49603|
user_list = []
data = 'userdata:2|eeeIP:127.0.0.1:56799|wwwIP:127.0.0.1:56800|aaaIP:127.0.0.1:56801|bbbIP:127.0.0.1:56802|'
user = ''
num = 0
for i in data[::-1]:
    user += i
    if i == '|':
        print(user[-2::-1])
        user_list.append(user[-2:0:-1])
        user = ' '
print(user_list[::])
i = len(user_list)
print(i,type(i))
# print('user倒序：', user)
# for i in user_list:
#     print(i)
# user_list.remove(' ')
#
#
#
# file = open('logo.txt', mode='a+',encoding='utf8',)
# file.write()
# file.close()

# def te(a, b, c):
#     print('a:',a)
#     print('b:',b)
#     print('c:',c)
#     return a, b, c
# i = te('',2,3)
# print(i)
# print(type(i))

# import random
# def makekey():
#     abc = ['a', 'b', 'c', 'e', 'f', 'A', 'B','C', 'E', 'F']
#     pd = random.randint(1111111111111111111, 9999999999999999999)
#     pdd_ = []
#     for i in str(pd):
#         pdd_.append(str(i))
#     # print(pdd_)
#     print(pd)
#     for g in str(pd):
#         pdd_[int(g)] = abc[int(g)]
#     # print(pdd_)
#     for i in pdd_:
#         print(i, end='')
#

    # print(key)

# makekey()

#
# def get_client(self):
#     while True:
#         client, address = self.server.accept()
#         server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + ']   客户端 ' + str(address[ 0 ]) + ':' \
#                       + str(address[ 1 ]) + ' 连接成功'
#         self.write_logs(server_info, '')
#         self.clients.append(client)
#         try:
#             client.send(self.data.encode())  # '已连接到服务器，请输入一个昵称'
#         except Exception as error:
#             server_info = '[系统消息' + ' ' + time.strftime("%H:%M:%S") + f']   消息发送失败，使线程未能启动，并与客户端的连接已断开。  |错误描述:{error}'
#             self.write_logs(server_info, '')
#             self.clients.remove(client)
#             client.close()
#         else:
#             #  启动多个线程
#             Thread(target=self.get_msg, args=(client, self.clients, self.clients_name_ip, address)).start()
#

# testlist = []
# print(len(testlist))
# testlist = [1,2,3,4,5]
# print(len(testlist))
# print(testlist[0])







