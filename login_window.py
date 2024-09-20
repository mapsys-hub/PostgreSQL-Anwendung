from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton
from PyQt6.QtCore import QObject, pyqtSignal


class LoginWindow(QWidget, QObject):
    login_submitted = pyqtSignal(str, str, str, str)

    def __init__(self):
        QWidget.__init__(self)
        QObject.__init__(self)
        self.setWindowTitle('Database Login')
        self.setGeometry(100, 100, 300, 150)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)
        self.user_edit = QLineEdit()
        self.user_edit.setText("postgres")#
        self.password_edit = QLineEdit()
        self.password_edit.setText("huber")#
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.name_edit = QLineEdit()
        self.name_edit.setText("office")
        self.host_edit = QLineEdit()
        self.host_edit.setText("192.168.1.232")
        self.port_edit = QLineEdit()
        self.port_edit.setText("5432")
        self.form_layout.addRow('Username:', self.user_edit)
        self.form_layout.addRow('Password:', self.password_edit)
        self.form_layout.addRow('Database:', self.name_edit)
        self.form_layout.addRow('Host:', self.host_edit)
        self.form_layout.addRow('Port:', self.port_edit)
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.read)
        self.layout.addWidget(self.login_button)

    def reset(self):
        self.user_edit.setText("")
        self.password_edit.setText("")
        self.name_edit.setText("office")
        self.host_edit.setText("192.168.1.232")
        self.port_edit.setText("5432")

    def read(self):
        name = self.name_edit.text()
        user = self.user_edit.text()
        password = self.password_edit.text()
        host = self.host_edit.text()
        port = self.port_edit.text()
        self.login_submitted.emit(user, password, host, name)
