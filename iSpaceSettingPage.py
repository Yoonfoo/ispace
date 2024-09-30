from PyQt6 import QtCore, QtWidgets
from datetime import datetime, timedelta
from CustomCalendar import CustomCalendarWidget

class ISpaceSettingPage(QtWidgets.QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.checkedDate_list = []
        self.setWindowTitle("ISpace Discussion Room")
        self.ui()
        # self.showMaximized()
        self.setFixedHeight(900)
        self.setFixedWidth(1440)

    def ui(self):
        
        layout_style = '''
            border: 1px solid #000;
            border-radius: 5px;
        '''

        label_style = '''
            border: None;
        '''

        select_style = '''
            border: 1px solid #000;
            border-radius: 0px;
        '''

        suspend_label_style = '''
            border: None;
            margin-left: 5px;
        '''

    ### #################################################################################

        layout_widget = QtWidgets.QWidget(self)
        layout_widget.setStyleSheet(layout_style)
        layout_widget.setGeometry(80,180,1300,500)
        # layout_widget.setGeometry(150,250,1500,500)
        self.layout = QtWidgets.QGridLayout(layout_widget)

    ### #################################################################################

        start_time = datetime.strptime('00:00', '%H:%M')
        end_time = datetime.strptime('23:59', '%H:%M')
        time_intervals = self.generate_time_intervals(start_time, end_time, 30)
        
    ### #################################################################################

        self.container_floor = QtWidgets.QWidget(self)
        self.floor = QtWidgets.QComboBox(self.container_floor)
        self.floor.setStyleSheet(select_style)
        self.floor.setFixedSize(150,30)
        self.floor.addItems(['','圖書館1F', '圖書館4F', '圖書館6F', '圖書館7F', '圖書館8F'])
        self.floor.currentIndexChanged.connect(self.rooms_selections)
        self.layout.addWidget(self.floor, 0, 0)
        self.layout.setAlignment(self.floor, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.setColumnMinimumWidth(0, 400)

    ### #################################################################################

        self.container = QtWidgets.QWidget(self)
        self.suspend_all = QtWidgets.QCheckBox(self.container)
        self.suspend_all.setText('暫停使用全部空間')
        self.suspend_all.setStyleSheet(label_style)
        self.suspend_all.setDisabled(True)
        self.suspend_all.clicked.connect(self.suspend_all_rooms)

        self.layout.addWidget(self.suspend_all, 1, 0)
        self.layout.setAlignment(self.suspend_all, QtCore.Qt.AlignmentFlag.AlignCenter)

    ### #################################################################################

        self.room_layout = QtWidgets.QHBoxLayout()
        self.room_1 = QtWidgets.QCheckBox(self)
        self.room_2 = QtWidgets.QCheckBox(self)
        self.room_3 = QtWidgets.QCheckBox(self)

        self.room_1.setStyleSheet(label_style)
        self.room_2.setStyleSheet(label_style)
        self.room_3.setStyleSheet(label_style)

        self.room_layout.addWidget(self.room_1)
        self.room_layout.addWidget(self.room_2)
        self.room_layout.addWidget(self.room_3)

        self.layout.addLayout(self.room_layout, 2, 0)
        self.room_1.setVisible(False)
        self.room_2.setVisible(False)
        self.room_3.setVisible(False)

    ### #################################################################################

        column_index = 1
        row_index = 0
        self.time_list = []
        
        for i in range(48):
            
            time = QtWidgets.QCheckBox(self)
            time.setText(time_intervals[i])
            time.setStyleSheet(label_style)
            time.clicked.connect(lambda checked, time=time: self.checked_date(time))

            self.time_list.append(time)
            self.layout.addWidget(time, row_index, column_index)
            column_index += 1

            if column_index == 9: 
                column_index = 1
                row_index += 1
    
    ### #################################################################################

        self.suspend_date_container_a = QtWidgets.QHBoxLayout()
        self.suspend_date_start = QtWidgets.QDateEdit(calendarPopup=True)
        self.suspend_date_start.setFixedSize(140,30)
        self.suspend_date_start.setDisplayFormat('yyyy/M/d')
        self.suspend_date_start.setDate(QtCore.QDate.currentDate())
        self.suspend_date_start_label = QtWidgets.QLabel(self)
        self.suspend_date_start_label.setFixedSize(130,30)
        self.suspend_date_start_label.setStyleSheet(suspend_label_style)
        self.suspend_date_start_label.setText('暫停開始日期: ')
        self.suspend_date_container_a.addWidget(self.suspend_date_start_label)
        self.suspend_date_container_a.addWidget(self.suspend_date_start)

        self.suspend_date_start_calendar = CustomCalendarWidget()
        self.suspend_date_start_calendar.setStyleSheet("""
            QCalendarWidget QWidget{
                border: None;
                                                       }
            QCalendarWidget QToolButton:hover {
                color: white;
                                                       }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: black;
                                                       }
        """)
        self.suspend_date_start.setMinimumDate(QtCore.QDate.currentDate())
        self.suspend_date_start.setCalendarWidget(self.suspend_date_start_calendar)

    ### #################################################################################

        self.suspend_date_container_b = QtWidgets.QHBoxLayout()
        self.suspend_date_end = QtWidgets.QDateEdit(calendarPopup=True)
        self.suspend_date_end.setFixedSize(140,30)
        self.suspend_date_end.setDisplayFormat('yyyy/M/d')
        self.suspend_date_end.setDate(QtCore.QDate.currentDate())
        self.suspend_date_end_label = QtWidgets.QLabel(self)
        self.suspend_date_end_label.setStyleSheet(suspend_label_style)
        self.suspend_date_end_label.setText('暫停結束日期 : ')
        self.suspend_date_end_label.setFixedSize(130, 30)
        self.suspend_date_container_b.addWidget(self.suspend_date_end_label)
        self.suspend_date_container_b.addWidget(self.suspend_date_end)

        self.suspend_date_end_calendar = CustomCalendarWidget()
        self.suspend_date_end_calendar.setStyleSheet("""
            QCalendarWidget QWidget{
                border: None;
                                                       }
            QCalendarWidget QToolButton:hover {
                color: white;
                                                       }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: black;
                                                       }
        """)
        self.suspend_date_end.setMinimumDate(QtCore.QDate.currentDate())
        self.suspend_date_end.setCalendarWidget(self.suspend_date_end_calendar)

        self.layout.addLayout(self.suspend_date_container_a, 3, 0)
        self.layout.addLayout(self.suspend_date_container_b, 4, 0)
      
    ### #################################################################################

        self.suspend_reason_container = QtWidgets.QHBoxLayout()
        self.suspend_reason_label = QtWidgets.QLabel(self)
        self.suspend_reason_label.setText('暫停使用原因: ')
        self.suspend_reason_label.setFixedSize(130,30)
        self.suspend_reason = QtWidgets.QLineEdit(self)
        self.suspend_reason.setFixedSize(140,30)
        self.suspend_reason_label.setStyleSheet(suspend_label_style)
        self.suspend_reason_container.addWidget(self.suspend_reason_label)
        self.suspend_reason_container.addWidget(self.suspend_reason)

        self.layout.addLayout(self.suspend_reason_container, 5, 0)

    ### #################################################################################

        self.add_suspend_button = QtWidgets.QPushButton(self)
        self.add_suspend_button.setText('新增暫停使用空間')
        self.add_suspend_button.setFixedSize(150,30)
        self.add_suspend_button.setStyleSheet('''
            QPushButton {
                border: 1px solid black;
                border-radius: 10px;
            }

            QPushButton:hover {
                background: black;
                color: white;
            }
        ''')
        self.add_suspend_button.clicked.connect(self.suspend_submit)
        self.layout.addWidget(self.add_suspend_button, 8, 7, 1, 2)

    ### #################################################################################

    def generate_time_intervals(self, start_time, end_time, interval_minutes):
        intervals = []
        current_time = start_time
        while current_time < end_time:
            end_interval = current_time + timedelta(minutes=interval_minutes - 1)
            intervals.append(f"{current_time.strftime('%H:%M')}~{end_interval.strftime('%H:%M')}")
            current_time += timedelta(minutes=interval_minutes)
        return intervals

    ### #################################################################################

    def rooms_selections(self):

        self.room_layout.setAlignment(self.room_1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.room_layout.setAlignment(self.room_2, QtCore.Qt.AlignmentFlag.AlignLeft)

        current_floors = self.floor.currentText()
        if current_floors == '':
            self.room_1.setVisible(False)
            self.room_2.setVisible(False)
            self.room_3.setVisible(False)
            self.suspend_all.setDisabled(True)

        elif current_floors == '圖書館1F':
            self.room_1.setVisible(True)
            self.room_2.setVisible(True)
            self.room_3.setVisible(False)
            self.room_1.setText('1A')
            self.room_2.setText('1B')
            self.suspend_all.setDisabled(False)

        elif current_floors == '圖書館4F':
            self.room_1.setVisible(True)
            self.room_2.setVisible(True)
            self.room_3.setVisible(True)
            self.room_1.setText('4A')
            self.room_2.setText('4B')
            self.room_3.setText('4C')
            self.suspend_all.setDisabled(False)
            self.room_layout.setAlignment(self.room_1, QtCore.Qt.AlignmentFlag.AlignRight)
            self.room_layout.setAlignment(self.room_2, QtCore.Qt.AlignmentFlag.AlignCenter)
            self.room_layout.setAlignment(self.room_3, QtCore.Qt.AlignmentFlag.AlignLeft)

        elif current_floors == '圖書館6F':
            self.room_1.setVisible(True)
            self.room_2.setVisible(True)
            self.room_3.setVisible(False)
            self.room_1.setText('6A')
            self.room_2.setText('6B')
            self.suspend_all.setDisabled(False)

        elif current_floors == '圖書館7F':
            self.room_1.setVisible(True)
            self.room_2.setVisible(True)
            self.room_3.setVisible(False)
            self.room_1.setText('7A')
            self.room_2.setText('7B')
            self.suspend_all.setDisabled(False)

        elif current_floors == '圖書館8F':
            self.room_1.setVisible(True)
            self.room_2.setVisible(True)
            self.room_3.setVisible(False)
            self.room_1.setText('8A')
            self.room_2.setText('8B')
            self.suspend_all.setDisabled(False)

    ### #################################################################################

    def checked_date(self, time):
        if time.isChecked():
            if time.text() not in self.checkedDate_list:
                self.checkedDate_list.append(time.text())
        else:
            if time.text() in self.checkedDate_list:
                self.checkedDate_list.remove(time.text())

    ### #################################################################################

    def suspend_all_rooms(self):

        self.room_1.setChecked(self.suspend_all.isChecked())
        self.room_2.setChecked(self.suspend_all.isChecked())
        self.room_3.setChecked(self.suspend_all.isChecked())

    ### #################################################################################

    def suspend_submit(self):
        start_date = self.suspend_date_start.date()
        end_date = self.suspend_date_end.date()

        if ((start_date == end_date) or (start_date > end_date)) and self.floor.currentText() != '':
            self.controller.click_automation(
                start_date, 
                self.floor.currentText(), 
                self.suspend_all.isChecked(), 
                self.room_1.isChecked(), 
                self.room_2.isChecked(),
                self.room_3.isChecked(), 
                self.checkedDate_list,
                self.suspend_reason.text()
                )
            
        elif end_date > start_date:
            while(start_date <= end_date):
                self.controller.click_automation(
                    start_date, 
                    self.floor.currentText(), 
                    self.suspend_all.isChecked(), 
                    self.room_1.isChecked(), 
                    self.room_2.isChecked(), 
                    self.room_3.isChecked(), 
                    self.checkedDate_list,
                    self.suspend_reason.text()
                    )
                start_date = start_date.addDays(1)

    