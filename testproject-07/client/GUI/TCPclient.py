from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel, Qt
from threading import Thread
import time
import sys
import socket

class TCPclient(QWidget):

    def __init__(self):
        QWidget.__init__(self, )
        #  GUI
        self.setGeometry(450, 200, 765, 415)
        self.setWindowTitle('多人聊天室')
        self.setFixedHeight(415)
        # 设置窗体背景颜色为白色
        self.setStyleSheet('TCPclient{background-color:white}')
        # 静态变量
        self.I = 0  # 控制窗口大小的变量
        # 调用方法
        self.change_gui()
        self.addgui()

    def addgui(self):
        """
        主界面的各个控件等
        :return:
        """
        #  消息框
        self.content1 = QTextBrowser(self)
        self.content1.setFont(QFont('微软雅黑', 12))
        self.content1.setGeometry(10, 10, 560, 300)
        self.content1.append('未连接到服务器')
        #  聊天室人数标签
        self.lable1 = QLabel('当前在线人数：0', self)
        self.lable1.setFont(QFont('微软雅黑', 10))
        self.lable1.setGeometry(590, 20, 200, 40)
        #  服务器状态标签
        self.lable2 = QLabel('服务器地址：', self)
        self.lable2.setFont(QFont('微软雅黑', 10))
        self.lable2.setGeometry(590, 6, 200, 20)
        #  IP输入框
        self.message2 = QLineEdit(self)
        self.message2.setPlaceholderText(u'输入服务端IP')
        # self.message2.setInputMask('000.000.000.000;')
        self.message2.setFont(QFont('微软雅黑', 11))
        self.message2.setGeometry(590, 60, 160, 25)
        self.list1 = [ '0.0.0.0','127.0.0.1' ]
        self.IP = QCompleter(self.list1)
        self.message2.setCompleter(self.IP)
        #  用户列表框
        self.list1 = QListView(self)
        self.data = QStringListModel()
        self.qList = [ '无用户' ]
        self.data.setStringList(self.qList)
        self.list1.setModel(self.data)
        self.list1.setFont(QFont('微软雅黑', 10))
        self.list1.setGeometry(590, 120, 160, 285)
        self.list1.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 用户列表不可编辑
        #  输入框
        self.message1 = QLineEdit(self)
        self.message1.setPlaceholderText(u'输入发送的内容')
        self.message1.setGeometry(10, 320, 560, 85)
        self.message1.setFont(QFont('微软雅黑', 14))
        self.message1.setAlignment(Qt.AlignTop)
        self.message1.returnPressed.connect(self.sendmsg)  # 回车触发
        #  清屏按钮
        self.button1 = QPushButton('清屏', self)
        self.button1.setFont(QFont('微软雅黑', 10, ))
        self.button1.setGeometry(410, 375, 40, 30)
        self.button1.setStyleSheet('border:1px solid black')
        self.button1.clicked.connect(self.cleartext)
        # self.button1.close()
        #  扩展按钮
        self.button2 = QPushButton('↑', self)
        self.button2.setGeometry(450, 375, 40, 30)
        self.button2.setStyleSheet('border:1px solid black')
        self.button2.clicked.connect(self.change_gui)
        #  连接按钮
        self.button3 = QPushButton('连接', self)
        self.button3.setFont(QFont('微软雅黑', 10, ))
        self.button3.setGeometry(590, 90, 80, 25)
        self.button3.setStyleSheet('border:1px solid black')
        self.button3.clicked.connect(self.connecttoserver)
        #  断开按钮
        self.button4 = QPushButton('断开', self)
        self.button4.setFont(QFont('微软雅黑', 10, ))
        self.button4.setGeometry(670, 90, 80, 25)
        self.button4.setStyleSheet('border:1px solid black')
        #  发送按钮
        self.button5 = QPushButton('发送', self)
        self.button5.setFont(QFont('微软雅黑', 12, ))
        self.button5.setGeometry(490, 375, 80, 30)
        self.button5.setStyleSheet('border:1px solid black')

    #  界面的宽度变化控制
    def change_gui(self):
        """
        在 21行 有一个变量I控制着窗体的大小
        :return:
        """
        if self.I == 1:
            self.setFixedWidth(765)
            self.I = 0
        else:
            self.setFixedWidth(581)
            self.I = 1

    #  清屏
    def cleartext(self):
        """
        确保在与客户端建立连接的状态下能够启用清屏功能
        :return: Null
        """
        if len(self.lable2.text()) > 7:
            self.content1.clear()

    #  连接到服务端
    def connecttoserver(self):
        """
        当处于未连接时按下连接按钮，将连接到服务器

        :return: Null
        """
        if len(self.lable2.text()) <= 7:
            IP = self.message2.text()
            PORT = 8899
            try:
                self.client = socket.socket()
                self.client.connect((IP, PORT))
            except Exception as error:
                self.content1.append(f'服务器可能未开始，请重试...\n请尝试关闭本地防火墙或允许8899端口\n错误描述：{error}')
                self.content1.moveCursor(self.content1.textCursor().End)
            else:
                self.content1.clear()
                self.lable2.setText(f'服务器地址：{IP}')
                self.workthread()

        else:
            if '当前已经连接到' not in self.content1.toPlainText():
                self.content1.append(f'当前已经连接到{self.message2.text()}\n')

    #  与服务端关闭连接
    def closewithserver(self):
        """
        当关闭与服务端的连接时，此方法会初始化在线人数标签、服务器地址标签、清除消息列表、在线用户列表等
        :return:
        """
        try:
            self.client.close()
            self.lable1.setText('当前在线人数：0')
            self.lable2.setText('服务器地址：')
            self.setWindowTitle('多人聊天室')
            self.content1.clear()
            self.qList.clear()
            self.data.setStringList(self.qList)
            self.list.setModel(self.data)
        except Exception as error:
            self.content1.append(f'当前未连接到服务器...\n错误描述：{error}')
            self.content1.moveCursor(self.content1.textCursor().End)

    #  接收信息
    def recvmgs(self):
        """
        接收从服务端发送的信息，并显示到消息框中
        其中，如果服务端的在线用户列表发生改变，则会发送一条消息头包含 ‘列表用户’ 的数据
        客户端如果匹配到用户列表数据则将本地的用户列表进行改变
        同时，在线用户标签也会根据用户列表的长度发生改变

        :return: Null
        """
        while True:
            time.sleep(0.1)
            try:
                data = self.client.recv(1024).decode() + '\n'
                if '列表用户' in data:
                    userlit = self.userlistdata(data[ :-1: ])
                    self.data1 = QStringListModel()
                    self.qList1 = userlit
                    self.data.setStringList(self.qList1)
                    self.lable1.setText(f'当前在线人数：{len(self.qList1)}')
                else:
                    if '欢迎' in data:
                        name = self.getnamebyserver(data)
                        self.setWindowTitle(f'多人聊天室  (当前用户：{name})')
                    self.content1.append(data)
                    self.content1.moveCursor(self.content1.textCursor().End)
            except Exception as error:
                self.content1.append(f'当前与服务器断开连接，请重新连接...\n{error}')
                self.content1.moveCursor(self.content1.textCursor().End)
                break

    #  发送信息
    def sendmsg(self):
        """
        一旦按下发送按钮，将发送框里的信息赋值给data变量，然后进行对服务器连接的判断，如果正在处于连接状态，将执行下一步骤
        判断消息是否是#quit，如果是则将消息发送至服务器，服务器会根据消息来源断开与客户端的连接
        如果是普通消息，则正常执行

        :return: Null
        """
        data = self.message1.text()
        if self.lable2.text() != '服务器地址：':
            if data == '#quit':
                try:
                    self.client.send(data.encode())
                except Exception as error:
                    self.content1.append(f'消息发送失败{error}')
                else:
                    self.closewithserver()
            else:
                try:
                    self.client.send(data.encode())
                except Exception as error:
                    self.content1.append(f'消息发送失败，错误信息{error}')
                    self.closewithserver()
            self.message1.clear()  # 消息框清屏

    #  获取用户昵称
    @staticmethod
    def getnamebyserver(data):
        """
        当服务端发送的消息中包含昵称，将对其处理，并返回用户名
        :param data: 服务端发送的包含昵称的消息
        :return: name
        """
        str = ''
        for i in data[16::]:
            str += i
            if i == '加':
                break
        return str[2:-1:]

    #  对用户列表的处理
    def userlistdata(self, data):
        """
        此方法是对服务端发送的用户列表信息进行处理，
        接收到服务端发送的用户信息后，对其进行切片，添加至列表等处理
        结果将返回一个用户的列表

        :param data:  接收到服务端的用户信息字符串
        :return: list:  返回一个包含有用户的列表
        """
        # 列表用户|user1[127.0.0.1:49768]|user2[127.0.0.1:49769]|
        s = ''
        list = [ ]
        try:
            for i in data[ 4:: ]:
                if i == '|':
                    continue
                elif i == ']':
                    i = ']\n'
                    s += i
                    list.append(s[ :-1: ])
                    s = ''
                else:
                    s += i
        except Exception:
            pass

        return list

    #  工作线程，许多功能不能只在一个线程中完成，需要用到多线程来实现
    def workthread(self):
        """
        工作线程
        :return: Null
        """
        Thread(target=self.closebtn).start()
        Thread(target=self.sendbtn).start()
        Thread(target=self.recvmgs).start()

    #  关闭按钮与closewithserver方法进行绑定
    def closebtn(self):
        """

        :return:
        """
        self.button4.clicked.connect(self.closewithserver)

    #  发送按钮与sendmsg方法进行帮绑定
    def sendbtn(self):
        """

        :return:
        """
        self.button5.clicked.connect(self.sendmsg)

    # 主窗体关闭进程终止
    def closeEvent(self, event):
        """
        重新定义了一遍当程序关闭时能够自觉的关闭自身进程
        :param event:
        :return:
        """
        try:
            self.closewithserver()
        except Exception:
            pass
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Tcpclient = TCPclient()
    Tcpclient.show()
    sys.exit(app.exec())
