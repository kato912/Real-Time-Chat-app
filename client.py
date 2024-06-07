from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
import requests


class chat_windown(QWidget):
    def __init__(self):
        super().__init__()
        #set Title
        self.setWindowTitle("Chat_app")
        #fix size windown
        self.setFixedSize(QSize(400,400))
        main_layout = QVBoxLayout()
        #user name
        username_layout = QHBoxLayout()
        text = QLabel("UserName:")
        self.inputname = QLineEdit()
        username_layout.addWidget(text)
        username_layout.addWidget(self.inputname)
        main_layout.addLayout(username_layout)
        #set up chat box ui
        self.chatBox = QListWidget()
        main_layout.addWidget(self.chatBox)
        #set input layout
        input_layout = QHBoxLayout()
        self.inputText = QLineEdit()
        self.inputText.returnPressed.connect(self.send_msg)
        input_layout.addWidget(self.inputText)
        
        send_but = QPushButton("Send")
        send_but.clicked.connect(self.send_msg)
        
        input_layout.addWidget(send_but)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)
        #delay for refresh messages
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ref_msg)
        self.timer.start(100)
        
    def send_msg(self):
        if self.inputname.text() == '':
            QMessageBox.information(self,'มีคนไม่กรอกชื่อครับจาร','กรอกชื่อของคุณก่อนน')
        elif self.inputText.text() == '':
            QMessageBox.information(self,"don't have message",'จะส่งข้อความแต่ไม่เขียนข้อความมันได้มั้ยหละเฮ้ย')
        else:
            # send message to server 
            text = f'{self.inputname.text()} : {self.inputText.text()}'
            send = requests.post('http://127.0.0.1:5000/send' , json={'msg':text})
            if send.status_code == 200:
                self.inputText.clear()
                self.ref_msg()
    def ref_msg(self):
        #load message form server 
        req = requests.get('http://127.0.0.1:5000/refmsg')
        if req.status_code == 200:
            msg = req.json()
            self.chatBox.clear()
            for i in msg:
                self.chatBox.addItem(i['msg'])
app = QCoreApplication.instance()
if app is None:
    app = QApplication([])
window = chat_windown()
window.show()
app.exec()