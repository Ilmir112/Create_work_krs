from PyQt6.QtWidgets import  QTableWidget
from PyQt6 import QtWidgets
from PyQt5 import QtCore
from PyQt6.QtCore import Qt



class TableWidget(QTableWidget):



    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)

        self.mouse_press = None

        # self.on_context_menu()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_press = "mouse left press"
        elif event.button() == Qt.MouseButton.RightButton:
            self.mouse_press = "mouse right press"
        elif event.button() == Qt.MouseButton.MidButton:
            self.mouse_press = "mouse middle press"
        super(TableWidget, self).mousePressEvent(event)



    def contextMenuEvent(self, event):
        from main import MyWindow
        print("Context menu event")
        menu = QtWidgets.QMenu(self)
        pervoration_action = menu.addAction("перфорация")
        pervoration_action.triggered.connect(lambda: MyWindow.openPerforation())
        about_action = menu.addAction("About")
        about_action.triggered.connect(
            lambda: print("About action triggered")
        )
        menu.exec(event.globalPos())
        return super().contextMenuEvent(event)









