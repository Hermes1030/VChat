from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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
        self.setStyleSheet('TCPclient{background-color:white}')  # 设置窗体背景颜色为白色
        # 静态变量
        self.I = 0  # 控制窗口大小的变量
        # 调用方法
        self.change_gui()
        self.add_gui()

    def add_gui(self):
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
        self.list1 = [ '0.0.0.0', '127.0.0.2', '127.0.0.1' ]
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
        self.message1.returnPressed.connect(self.sendMsg)  # 回车触发
        #  清屏按钮
        self.button1 = QPushButton('清屏', self)
        self.button1.setFont(QFont('微软雅黑', 10, ))
        self.button1.setGeometry(410, 375, 40, 30)
        self.button1.setStyleSheet('border:1px solid black')
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
        self.button3.clicked.connect(self.connectToserver)
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

    #  GUI的宽度变化
    def change_gui(self):
        if self.I == 1:
            self.setFixedWidth(765)
            self.I = 0
        else:
            self.setFixedWidth(581)
            self.I = 1

    def recvMsg(self):
        while True:
            time.sleep(0.5)
            try:
                data = self.client.recv(1024).decode() + '\n'
                if '列表用户' in data:
                    userlit = self.dateUserlist(data[:-1:])
                    self.data1 = QStringListModel()
                    self.qList1 = userlit
                    self.data.setStringList(self.qList1)
                    self.lable1.setText(f'当前在线人数：{len(self.qList1)}')
                else:
                    self.content1.append(data)
                    self.content1.moveCursor(self.content1.textCursor().End)
            except Exception as error:
                self.content1.append(f'与服务器断开连接...\n{error}')
                self.content1.moveCursor(self.content1.textCursor().End)
                break

    def sendMsg(self):
        data = self.message1.text()
        if self.lable2.text() != '服务器地址：':
            if data == '#quit':
                try:
                    self.client.send(data.encode())
                except Exception as error:
                    self.content1.append(f'消息发送失败{error}')
                else:
                    self.closeWithserver()
            else:
                try:
                    self.client.send(data.encode())
                except Exception as error:
                    self.content1.append(f'消息发送失败，错误信息{error}')
                    self.closeWithserver()
            self.message1.clear()

    def connectToserver(self):
        if len(self.lable2.text()) <= 7:
            IP = self.message2.text()
            PORT = 8899
            try:
                self.client = socket.socket()
                self.client.connect((IP, PORT))
            except Exception as error:
                self.content1.append(f'服务器可能未开始，请重试...\n错误描述：{error}')
                self.content1.moveCursor(self.content1.textCursor().End)
            else:
                self.content1.clear()
                self.lable2.setText(f'服务器地址：{IP}')
                self.work_thread()

        else:
            if '当前已经连接到' not in self.content1.toPlainText():
                self.content1.append(f'当前已经连接到{self.message2.text()}')

    def closeWithserver(self):
        try:
            self.client.close()
            self.lable1.setText('当前在线人数：0')
            self.lable2.setText('服务器地址：')
            self.content1.clear()
            self.qList.clear()
            self.data.setStringList(self.qList)
            self.list.setModel(self.data)
        except Exception as error:
            self.content1.append(f'当前未连接到服务器...\n错误描述：{error}')
            self.content1.moveCursor(self.content1.textCursor().End)

    def dateUserlist(self, data):
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

    def work_thread(self):
        Thread(target=self.close_btn).start()
        Thread(target=self.send_btn).start()
        Thread(target=self.recvMsg).start()

    def close_btn(self):
        self.button4.clicked.connect(self.closeWithserver)

    def send_btn(self):
        self.button5.clicked.connect(self.sendMsg)

    # 主窗体关闭进程终止
    def closeEvent(self, event):
        try:
            self.closeWithserver()
        except Exception:
            pass
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Tcpclient = TCPclient()
    Tcpclient.show()
    sys.exit(app.exec())
