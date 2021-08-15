from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread
import time
import sys
import socket

#  复盘在线列表

class TCPclient(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #  GUI
        self.setGeometry(450, 200, 601, 409)
        self.setWindowTitle('多人聊天室')
        self.I = 0  # 控制窗口大小的变量
        self.setFixedHeight(409)
        #  调用方法
        self.change_gui()
        self.add_gui()

    def add_gui(self):
        #  消息框
        self.content = QTextBrowser(self)
        self.content.setFont(QFont('微软雅黑', 12))
        self.content.setGeometry(10, 10, 560, 300)
        self.content.append('未连接到服务器')
        #  聊天室人数标签
        self.lable = QLabel('当前在线人数：0', self)
        self.lable.setFont(QFont('微软雅黑', 10))
        self.lable.setGeometry(590, 20, 200, 40)
        #  服务器状态标签
        self.lable2 = QLabel('服务器地址：', self)
        self.lable2.setFont(QFont('微软雅黑', 10))
        self.lable2.setGeometry(590, 6, 200, 20)
        #  IP输入框
        self.message2 = QLineEdit(self)
        self.message2.setPlaceholderText(u'输入服务端IP')
        # self.message2.setInputMask('000.000.000.000;')
        self.message2.setFont(QFont('黑体', 11))
        self.message2.setGeometry(590, 60, 160, 25)
        self.list1 = [ '默认', '0.0.0.0', '127.0.0.2', '127.0.0.1' ]
        self.IP = QCompleter(self.list1)
        self.message2.setCompleter(self.IP)
        #  连接按钮
        self.button3 = QPushButton('连接', self)
        self.button3.setGeometry(590, 90, 80, 25)
        self.button3.clicked.connect(self.con_server)
        #  断开按钮
        self.button4 = QPushButton('断开', self)
        self.button4.setGeometry(670, 90, 80, 25)
        self.button4.close()
        #  用户列表框
        self.list = QListView(self)
        self.data = QStringListModel()
        #
        self.qList = [ '无用户' ]
        self.data.setStringList(self.qList)
        self.list.setModel(self.data)
        self.list.setFont(QFont('黑体', 10))
        self.list.setGeometry(590, 120, 160, 275)
        self.list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #  输入框
        self.message = QLineEdit(self)
        self.message.setPlaceholderText(u'输入发送的内容')
        self.message.setGeometry(10, 320, 560, 50)
        self.message.setFont(QFont('黑体', 14))
        self.message.setAlignment(Qt.AlignTop)
        self.message.returnPressed.connect(self.send_msg)
        #  发送按钮
        self.button = QPushButton('发送', self)
        self.button.setFont(QFont('微软雅黑', 10, QFont.Bold))
        self.button.setGeometry(491, 375, 80, 30)
        # self.button.close()
        #  扩展按钮
        self.button2 = QPushButton('↑', self)
        self.button2.setGeometry(450, 375, 40, 30)
        self.button2.clicked.connect(self.change_gui)
        #  清屏按钮
        self.button1 = QPushButton('清屏', self)
        self.button1.setGeometry(410, 375, 40, 30)
        self.button1.close()
        self.button1.clicked.connect(self.clear_mag)

    #  GUI的宽度变化
    def change_gui(self):
        if self.I == 1:
            self.setFixedWidth(765)
            self.I = 0
        else:
            self.setFixedWidth(581)
            self.I = 1

    #  connect to server
    def con_server(self):
        #  socket 套接字
        IP = self.message2.text()
        if IP == '默认':
            IP = '127.0.0.1'
        PORT = 8899
        try:
            self.client = socket.socket()
            self.client.connect((IP, PORT))
        except Exception as error:
            self.content.append(f'服务器可能未开启，请重试...\n错误描述：{error}')
            self.content.moveCursor(self.content.textCursor().End)
        else:
            self.content.clear()
            self.work_thread()
            # self.change_gui()
            self.button3.close()
            self.button4.show()
            self.button1.show()
            self.lable2.setText(f'服务器地址：{IP}')
            # self.qList[ 0 ] = '-------在线列表-------'
            # self.data.setStringList(self.qList)
            Thread(target=self.btn_close).start()

    #  关闭连接
    def close_connect(self):
        try:
            self.client.close()
            # self.content.clear()
            self.lable.setText('当前在线人数：0')
            self.lable2.setText('服务器地址：')
            self.setWindowTitle(f'多人聊天室')
            self.qList.clear()
            self.data.setStringList(self.qList)
            self.list.setModel(self.data)
        except Exception as error:
            self.content.append(f'当前未连接到服务器...\n错误描述：{error}')
            self.content.moveCursor(self.content.textCursor().End)
        else:
            self.button3.show()
            self.button4.close()
            self.button1.close()

    #  清屏按钮事件
    def clear_mag(self):
        self.content.clear()

    #  处理发送消息
    def send_msg(self):
        msg = self.message.text()
        if msg.upper() == '#CLEAR':
            self.content.clear()
        else:
            time.sleep(0.1)
            if self.lable2.text() != '服务器地址：':
                self.client.send(msg.encode())
        if msg.upper() == '#QUIT':
            self.client.close()
            self.destroy()
            sys.exit(0)  # 退出进程
        #  编辑区清空
        self.message.clear()

    #  处理接收到的消息
    def recv_msg(self):
        while True:
            time.sleep(0.1)
            try:
                data = self.client.recv(1024).decode()
                # s = ''
                #  窗体标题[用户名]加载槽
                # if '欢迎' in data:
                #     for i in data[ 18:: ]:
                #         s = s + i
                #         if i == '加':
                #             break
                #     self.setWindowTitle(f'多人聊天室（当前用户名：{s[ :-1 ]}）')
                #  标签[在线人数]槽
                # if 'userdata:' in data:
                #     num = data[ 9 ]
                #     self.lable.setText(f'当前在线人数：{num}')
                    # self.user_list(num, data)
                #  消息窗口[消息]槽
                # else:
                data = data + '\n'
                self.content.append(data)  # 将收到的消息显示到消息框
                #  始终显示最后一行
                self.content.moveCursor(self.content.textCursor().End)
            except Exception as error:
                self.content.append(f'与服务器断开连接...\n错误描述：{error}')
                self.close_connect()
                self.content.moveCursor(self.content.textCursor().End)
                break

    # def user_list(self, num, data):
    #     self.qList = [ ]
    #     users = [ ]
    #     user = ' '
    #     for i in data[ ::-1 ]:
    #         user += i
    #         if i == '|':
    #             users.append(user[ -2:0:-1 ])
    #             user = ' '
    #     print(users)
    #     time.sleep(0.1)
    #     if len(self.qList) == 1:
    #         for i1 in users[1::]:
    #             self.qList.append(i1)
    #             self.data.setStringList(self.qList)
    #             self.list.setModel(self.data)
    #     if len(self.qList) > 1:
    #         if self.qList[1] != users[1]:
    #             self.qList.append(users[1])
    #             self.data.setStringList(self.qList)
    #             self.list.setModel(self.data)

    #  发送按钮单机事件
    def btn_send(self):
        self.button.clicked.connect(self.send_msg)

    #  断开按钮单机事件
    def btn_close(self):
        self.button4.clicked.connect(self.close_connect)

    #  多线程启动
    def work_thread(self):
        Thread(target=self.btn_send).start()
        Thread(target=self.recv_msg).start()

    # 主窗体关闭进程终止
    def closeEvent(self, event):
        self.close_connect()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = TCPclient()
    client.show()
    sys.exit(app.exec())
