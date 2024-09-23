from PyQt6 import QtWidgets, QtGui, QtCore

class CustomCalendarWidget(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGridVisible(True)
        self.setNavigationBarVisible(True)
        self.setMinimumDate(QtCore.QDate.currentDate())
        self.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

    def paintCell(self, painter: QtGui.QPainter, rect: QtCore.QRect, date: QtCore.QDate):
        # Call the base class implementation to draw the standard calendar cell
        super().paintCell(painter, rect, date)

        # Check if the date is in the previous or next month
        current_month = self.monthShown()
        # if (date.month() < current_month) or (date.month() > current_month or date.month() != (current_month % 12) + 1):
        if (date < self.minimumDate()) or (date.month() < current_month) or (date.month() > current_month) or (date.year() > self.yearShown()):
            # Set the background color for previous and next month dates
            painter.fillRect(rect, QtGui.QColor(200, 200, 200))  # Light gray background
            
        # Draw the date text
        painter.setPen(QtGui.QColor(0, 0, 0))  # Black text color
        painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, str(date.day()))