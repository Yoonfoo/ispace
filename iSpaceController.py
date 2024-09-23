from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread
from playwright.sync_api import sync_playwright

class IspaceController(QThread):
    
    pixmap_ready = QtCore.pyqtSignal(QPixmap)
    clear_widget = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.page = None

    def capture_login_page(self):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://ispace-lis.nsysu.edu.tw/manager/loginmgr.aspx')
        
        clip_area = {
            'x': 760,
            'y': 325,
            'width': 150,
            'height': 26
        }
        screenshot = page.screenshot(clip=clip_area)
        self.page = page
        return screenshot

    def on_login_button_clicked(self, userID, pwd, vc):
        # Fetch text from input fields and call the do_setting method
        id = self.page.get_by_placeholder('請輸入系統登入帳號')
        pw =  self.page.get_by_placeholder('請輸入系統登入密碼')
        captcha =  self.page.get_by_placeholder('請輸入認證文字')
        login_button =  self.page.get_by_title('登 入')

        id.fill(userID)
        pw.fill(pwd)
        captcha.fill(vc)
        login_button.click()
        self.page.wait_for_load_state('load')

        if self.page.url == 'https://ispace-lis.nsysu.edu.tw/manager/loginmgr.aspx':
            return
        else:
            self.clear_widget.emit()
            self.page.frame_locator('#mainframe').get_by_title('空間管理').click()
            self.page.frame_locator('#subframe').get_by_title('小型討論室').click()
            self.page.frame_locator('#subframe').get_by_title('討論室暫停使用列表').first.click()        
    
    def display_screenshot(self):
        screenshot_generator = self.capture_login_page()

        pixmap = QPixmap()
        pixmap.loadFromData(QtCore.QByteArray(screenshot_generator))
        self.pixmap_ready.emit(pixmap)