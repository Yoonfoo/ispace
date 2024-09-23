import asyncio
import sys
from datetime import datetime, timedelta
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread
from playwright.sync_api import sync_playwright
from iSpaceController import IspaceController
from iSpaceSettingPage import ISpaceSettingPage

class ISpaceLoginPage(QtWidgets.QWidget):

    pixmap_ready = QtCore.pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ISpace Settings")
        self.resize(500,300)
    
        self.controller = IspaceController()
        self.controllerThread = QThread()
        self.controller.moveToThread(self.controllerThread)
        self.controllerThread.start()
        self.controller.pixmap_ready.connect(self.display_pixmap)
        self.controller.clear_widget.connect(self.clear_all_widgets)
        self.ui()

    def ui(self):

        style_box = '''
            background:#fff;
            padding: 5px;
            border: None;
        '''

        info_style = '''
            border: None;
            text-align: end;
        '''

        input_bar_style = '''
            border: 1px solid black;
            border-radius: 10px;
            padding-right: 50px;
        '''

        captcha_style = '''
            border: None;
        '''

        grid_box = QtWidgets.QWidget(self)
        grid_box.setGeometry(0,0,500,300)
        grid_box.setStyleSheet(style_box)
        self.grid_layout = QtWidgets.QGridLayout(grid_box)

        self.userID = QtWidgets.QLabel(self)
        self.password = QtWidgets.QLabel(self)
        self.captcha = QtWidgets.QLabel(self)
        self.userID.setText("User ID: ")
        self.password.setText("Password: ")
        self.captcha.setText("Verification Code: ")
        self.userID.setStyleSheet(info_style)
        self.password.setStyleSheet(info_style)
        self.captcha.setStyleSheet(info_style)


        self.idInput = QtWidgets.QLineEdit(self)
        self.pwInput = QtWidgets.QLineEdit(self)
        self.captchaInput = QtWidgets.QLineEdit(self)
        self.image_label = QtWidgets.QLabel(self)
        self.loginButton = QtWidgets.QPushButton(self)
        self.loginButton.setText("Login")
        self.idInput.setStyleSheet(input_bar_style)
        self.pwInput.setStyleSheet(input_bar_style)
        self.captchaInput.setStyleSheet(input_bar_style)
        self.loginButton.setStyleSheet('''
            QPushButton {
                border: 1px solid black;
                border-radius: 10px;
            }

            QPushButton:hover {
                background: black;
                color: white;
            }
        ''')
        
        self.pwInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.image_label.setStyleSheet(captcha_style)

        self.controller.display_screenshot()

        self.grid_layout.addWidget(self.userID, 0, 0)
        self.grid_layout.addWidget(self.password, 1, 0)
        self.grid_layout.addWidget(self.captcha, 2, 0)
        self.grid_layout.addWidget(self.idInput, 0, 1)
        self.grid_layout.addWidget(self.pwInput, 1, 1)
        self.grid_layout.addWidget(self.captchaInput, 2, 1)
        self.grid_layout.addWidget(self.image_label, 2, 2)
        self.grid_layout.addWidget(self.loginButton, 3, 1)

        self.loginButton.clicked.connect(lambda: self.controller.on_login_button_clicked(self.idInput.text(), self.pwInput.text(), self.captchaInput.text()))

    def clear_all_widgets(self):
        
        # while self.grid_layout.count():
        #     item = self.grid_layout.takeAt(0)
        #     widget = item.widget()
        #     if widget:
        #         widget.deleteLater()
        
        # self.grid_layout.deleteLater()
        # self.deleteLater()
        self.setting_window = ISpaceSettingPage(self.controller.page)
        self.setting_window.show()

        self.close()

    # @QtCore.pyqtSlot(QPixmap)
    def display_pixmap(self,pixmap):
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedHeight(50)
        self.image_label.setFixedWidth(160)

    def center_window(self):
        # Get the screen size
        screen = QtWidgets.QApplication.screens()
        screen_size = screen[0].size()
        print(screen_size)
        screen_w = screen_size.width()
        screen_h = screen_size.height()

        w = self.width()
        h = self.height()

        center_x = int((screen_w - w)/2)
        center_y = int((screen_h - h)/2)
        self.move(center_x, center_y)

    def keyPressEvent(self, event):
        keycode = event.key()
        if keycode == QtCore.Qt.Key.Key_Return or keycode == QtCore.Qt.Key.Key_Enter:
            self.controller.on_login_button_clicked(self.idInput.text(), self.pwInput.text(), self.captchaInput.text())



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = ISpaceLoginPage()
    controller.show()
    
    sys.exit(app.exec())