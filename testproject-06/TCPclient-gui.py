from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread
import time
import sys
import socket

class TCPclient(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # main
        self.setGeometry(400, 200, 590, 410)
        self.setWindowTitle('多人聊天室')
        self.setFixedHeight(410)
        self.setFixedWidth(590)
        self.setStyleSheet('TCPclient{background-color:white}')  # 设置窗体背景颜色为白色

        #  function
        self.gui()
        #  connect to server
        self.connect_server()
    def gui(self):
        #  消息框
        self.content1 = QTextBrowser(self)
        self.content1.setFont(QFont('微软雅黑', 12))
        self.content1.setGeometry(0, 0, 400, 320)
        #  输入框
        self.message = QTextEdit(self)
        self.message.setPlaceholderText(u'输入发送的内容')
        self.message.setGeometry(0, 330, 400, 80)
        self.message.setFont(QFont('黑体', 12))
        self.message.setAlignment(Qt.AlignTop)
        #  发送按钮
        self.button1 = QPushButton('发送', self)
        self.button1.setFont(QFont('微软雅黑', 9))
        self.button1.setGeometry(300, 380, 70, 30)
        self.button1.setStyleSheet('QPushButton{background-color:skyblue}')
        #  设置按钮
        self.button2 = QPushButton('···', self)
        self.button2.setFont(QFont('微软雅黑', 11))
        self.button2.setGeometry(370, 380, 30, 30)
        self.button2.setStyleSheet('QPushButton{background-color:skyblue}')
        #  系统提示框
        self.content2 = QTextBrowser(self)
        self.content2.setFont(QFont('微软雅黑', 8))
        self.content2.setGeometry(410, 0, 180, 160)
        #  用户列表框
        self.list = QListView(self)
        self.data = QStringListModel()
        self.qList = [ 'user1' ]
        self.data.setStringList(self.qList)
        self.list.setModel(self.data)
        self.list.setFont(QFont('黑体', 10))
        self.list.setGeometry(410, 170, 180, 240)
        self.list.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def connect_server(self):
        self.client = socket.socket()
        self.client.connect(('127.0.0.1', 8899))
        self.work()
    def recv_msg(self):
        while True:
            time.sleep(0.1)
            recv_msg = self.client.recv(1024).decode()
            self.content1.append(recv_msg)
    def send_msg(self):
        text = self.message.toPlainText()
        self.client.send(text.encode())
        if text == 'quit':
            self.client.close()
        self.message.clear()
    def btn_send(self):
        self.button1.clicked.connect(self.send_msg)
    def work(self):
        Thread(target=self.btn_send).start()
        Thread(target=self.recv_msg).start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    CLIENT = TCPclient()
    CLIENT.show()
    sys.exit(app.exec())