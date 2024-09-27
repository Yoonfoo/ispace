from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread
from datetime import datetime
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

    def click_automation(self, start_date, floor, suspend_all, room_1, room_2, checkedDate_list,suspend_reason):
        
        self.page.frame_locator('#contentframe').frame_locator('#iframePage').get_by_title('新增暫停使用空間').click()

        try:
            self.page.frame_locator('#contentframe').locator('#floor').select_option(floor)
            self.page.wait_for_timeout(500)
                
            if suspend_all:
                self.page.frame_locator('#contentframe').locator('label.chkboxAll').set_checked(True)
            elif room_1:
                self.page.frame_locator('#contentframe').locator('label.chksel').nth(0).set_checked(True)
            elif room_2:
                self.page.frame_locator('#contentframe').locator('label.chksel').nth(1).set_checked(True)
            
            self.page.frame_locator('#contentframe').locator('input.YYYYMMDD').click()

            date = datetime.strptime(start_date.toString('yyyy/MM'), "%Y/%m")
            calender_date = datetime.strptime(
                self.page.frame_locator('#contentframe').locator('div.nav').locator('a.yyyymmdd').inner_html(), "%Y/%m")
            diff = (date.year - calender_date.year) * 12 + (date.month - calender_date.month)
                
            if diff != 0:
                for i in range(diff):
                    self.page.frame_locator('#contentframe').locator('div.nav').locator('a.monthR').click()
            
            self.page.frame_locator('#contentframe').locator('div.calendar').get_by_title(start_date.toString('yyyy/MM/d'), exact=True).click()#.locator('table.calendar').click()
            self.page.frame_locator('#contentframe').locator('input.textNeed').nth(1).clear()
            self.page.frame_locator('#contentframe').locator('input.textNeed').nth(1).fill(suspend_reason)


            if len(checkedDate_list) == 0:
                self.page.frame_locator('#contentframe').locator('div.pagefun').nth(0).get_by_title('新增暫停使用空間').click()
            else:
                for time in checkedDate_list:
                    self.page.frame_locator('#contentframe').get_by_text(time).click()
                self.page.frame_locator('#contentframe').locator('div.pagefun').nth(0).get_by_title('新增暫停使用空間').click()

        except:
            pass