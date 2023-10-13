from PyQt5.QtWidgets import QTableWidget, QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from work_py.perforation import PervorationWindow


class TableWidget(QTableWidget):
    perforation_window = None
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)
        self.mouse_press = None

        # self.on_context_menu()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_press = "mouse left press"
        elif event.button() == Qt.MouseButton.RightButton:
            self.mouse_press = "mouse right press"

        # elif event.button() == Qt.MouseButton.MidButton:
        #     self.mouse_press = "mouse middle press"
        super(TableWidget, self).mousePressEvent(event)



    # def openPerforation(self):
    #     import sys
    #     if TableWidget.perforation_window is None:
    #         app = QtWidgets.QApplication(sys.argv)
    #         self.perforation_window = PervorationWindow()
    #         self.perforation_window.show()
    #         sys.exit(app.exec_())
    #
    #     else:
    #         self.perforation_window.close()  # Close window.
    #         self.perforation_window = None  # Discard reference.










