import random

'''
消息的发出与接收需要解码
send encode
recv decode
'''

#  生成编码
def make_key(self):
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

    #  保存聊天记录
    #  保存日志
