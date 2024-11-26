from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QWidget, QLabel, QComboBox, QGridLayout,  QPushButton

import data_list

from .parent_work import TabWidgetUnion, TabPageUnion, WindowUnion



class TabPageSoCurator(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.curator_label = QLabel("Куратор", self)
        self.curator_combo = QComboBox(self)
        curator_list = ['ГРР', 'ОР', 'ГТМ', 'ГО', 'ВНС']
        self.curator_combo.addItems(curator_list)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.curator_label, 2, 0)
        self.grid.addWidget(self.curator_combo, 3, 0)


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoCurator(parent), 'Куратор')


class SelectCurator(WindowUnion):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.tabWidget = TabWidget(parent)

        self.buttonadd_work = QPushButton('Изменить')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)

        vbox = QGridLayout(self.centralWidget)

        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonadd_work, 3, 0)

    def add_work(self):
        curator_combo = self.tabWidget.currentWidget().curator_combo.currentText()
        self.data_well.curator = curator_combo

        data_list.pause = False
        self.close()



