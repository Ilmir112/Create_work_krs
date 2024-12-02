from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

import data_list
from gnkt_data.gnkt_data import dict_saddles
from main import MyMainWindow
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion


class TabPageSo(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        manufacturer_list = ['НТЦ ЗЭРС', 'Зенит', 'Барбус']


        self.labels_plast = {}
        self.dict_perforation = self.data_well.dict_perforation
        plast_all = list(self.dict_perforation.keys())[0]

        self.number_port_label = QLabel("номер порта")
        self.roof_label = QLabel("Кровля")
        self.sole_label = QLabel("Подошва")
        self.type_saddles_label = QLabel("Тип хвостовика")

        self.diameter_saddles_label = QLabel("Диаметр седла")
        self.diameter_ball_label = QLabel("Диаметр шара")
        self.type_column_label = QLabel('Тип колонны')
        self.type_column_edit = QLineEdit(self)

        self.manufacturer_label = QLabel("Подрядчик хвостовика")
        self.manufacturer_combo = QComboBox(self)
        self.manufacturer_combo.addItems(manufacturer_list)

        self.grid.addWidget(self.number_port_label, 0, 0)
        self.grid.addWidget(self.roof_label, 0, 1)
        self.grid.addWidget(self.sole_label, 0, 2)
        self.grid.addWidget(self.type_saddles_label, 0, 3)
        self.grid.addWidget(self.diameter_saddles_label, 0, 4)
        self.grid.addWidget(self.diameter_ball_label, 0, 5)
        self.grid.addWidget(self.manufacturer_label, 8, 3)
        self.grid.addWidget(self.manufacturer_combo, 9, 3)
        self.grid.addWidget(self.type_column_label, 10, 3)
        self.grid.addWidget(self.type_column_edit, 11, 3)

        index_interval = 1
        for index, (roof, sole) in enumerate(
                list(sorted(self.dict_perforation[plast_all]["интервал"], key=lambda x: x[0], reverse=True))):
            self.number_port = QLabel(self)
            self.number_port.setText(f'Муфта №{index_interval}')

            self.roof_edit = QLineEdit(self)
            self.roof_edit.setText(str(roof))

            self.sole_edit = QLineEdit(self)
            self.sole_edit.setText(str(sole))

            self.type_saddles_ComboBox = QComboBox(self)
            # self.type_saddles_ComboBox.addItems(self.type_saddles_list)
            self.type_saddles_ComboBox.currentIndexChanged.connect(
                lambda i, idx=index: self.on_type_saddles_change(i, idx, self.type_saddles_ComboBox))

            self.diameter_saddles_edit = QLineEdit(self)
            self.diameter_ball_edit = QLineEdit(self)

            self.grid.addWidget(self.number_port, index_interval, 0)
            self.grid.addWidget(self.roof_edit, index_interval, 1)
            self.grid.addWidget(self.sole_edit, index_interval, 2)
            self.grid.addWidget(self.type_saddles_ComboBox, index_interval, 3)
            self.grid.addWidget(self.diameter_saddles_edit, index_interval, 4)
            self.grid.addWidget(self.diameter_ball_edit, index_interval, 5)

            setattr(self, f"plast_{index_interval}_edit", self.number_port)
            setattr(self, f"roof_{index_interval}_edit", self.roof_edit)
            setattr(self, f"sole_{index_interval}_edit", self.sole_edit)
            setattr(self, f"type_status_{index}_edit", self.type_saddles_ComboBox)
            setattr(self, f"diameter_saddles_{index_interval}_edit", self.diameter_saddles_edit)
            setattr(self, f"diameter_ball_{index_interval}_edit", self.diameter_ball_edit)

            self.labels_plast[index] = [self.number_port.text(), self.roof_edit.text(), self.sole_edit.text(),
                                        self.type_saddles_ComboBox, self.diameter_saddles_edit, self.diameter_ball_edit]
            self.labels_plast_read = {}

            index_interval += 1

        self.manufacturer_combo.currentIndexChanged.connect(
            lambda index: self.check_manufacturer(plast_all))
        self.manufacturer_combo.setCurrentIndex(1)

    def check_manufacturer(self, plast):

        if self.manufacturer_combo.currentText() == 'НТЦ ЗЭРС':
            self.manufacturer = 'НТЦ ЗЭРС'
            if (self.data_well.column_additional and self.data_well.column_additional_diameter.get_value < 110) \
                    or self.data_well.column_additional is False and self.data_well.column_diameter.get_value < 110:
                self.type_column = "ФПЗН.102"

            else:
                self.type_column = "ФПЗН1.114"

        elif self.manufacturer_combo.currentText() == 'Зенит':
            self.manufacturer = 'Зенит'
            self.type_column = "ФПЗН1.114"


        elif self.manufacturer_combo.currentText() == 'Барбус':
            self.manufacturer = 'Барбус'
            self.type_column = "гидравлич"

        self.type_column_edit.setText(self.type_column)

        if self.type_column == "ФПЗН.102" and self.manufacturer == 'НТЦ ЗЭРС':
            self.type_saddles_list = ['102/70', '102/67', '102/64', '102/61', '102/58', '102/55', '102/52', '102/49',
                                      '102/47', '102/45']

        elif self.type_column == "ФПЗН1.114" and self.manufacturer == 'НТЦ ЗЭРС':
            self.type_saddles_list = ['114/70А', '114/67А', '114/64А', '114/61А', '114/58А', '114/55А', '114/52А',
                                      '114/49А', '114/47А', '114/45А']
        elif self.type_column == "ФПЗН1.114" and self.manufacturer == 'Зенит':
            self.type_saddles_list = ['1.952"', '2,022"', '2,092"', '2,162"', '114/58А', '2,322"',
                                      '2,402"', '2,487"', '2,577"', '2,667"', '2,757"', '2,547"']
        elif self.manufacturer == 'Барбус':
            self.type_saddles_list = ['51,36t20', '54,00t20', '56,65t20', '59,80t20',
                                      '62,95t20', '66,10t20']
        # self.type_column_edit.textChanged(self.check_type_column)

        for index in range(len(self.dict_perforation[list(self.dict_perforation.keys())[0]]["интервал"])):
            self.type_saddles_ComboBox = QComboBox(self)
            # print(self.type_saddles_list)
            self.type_saddles_ComboBox.currentIndexChanged.connect(
                lambda i, idx=index: self.on_type_saddles_change(i, idx, self.type_saddles_ComboBox))
            self.type_saddles_ComboBox.addItems(self.type_saddles_list)
            self.grid.addWidget(self.type_saddles_ComboBox, index + 1, 3)
            setattr(self, f"type_status_{index}_edit", self.type_saddles_ComboBox)

    def on_type_saddles_change(self, idx, index_interval, type_saddles_ComboBox):
        # print(f'индекс {idx}')
        # Получаем текст из выбранного элемента в type_saddles_ComboBox
        type_items = [type_saddles_ComboBox.itemText(i) for i in range(type_saddles_ComboBox.count())]
        # print(f'tyo работает {idx, index_interval, type_items[idx]}')
        # Получаем данные о шаре и седле для выбранного типа

        self.diameter_saddles_edit = QLineEdit(self)
        self.diameter_ball_edit = QLineEdit(self)

        diameter_saddles = dict_saddles[self.manufacturer][self.type_column][type_items[idx]].saddle
        self.diameter_saddles_edit.setText(diameter_saddles)
        diameter_ball = dict_saddles[self.manufacturer][self.type_column][type_items[idx]].ball
        self.diameter_ball_edit.setText(diameter_ball)

        self.grid.addWidget(self.diameter_saddles_edit, index_interval + 1, 4)
        self.grid.addWidget(self.diameter_ball_edit, index_interval + 1, 5)

        setattr(self, f"diameter_saddles_{index_interval}_edit", diameter_saddles)
        setattr(self, f"diameter_ball_{index_interval}_edit", diameter_ball)

        self.labels_plast[index_interval][3] = type_items[idx]
        self.labels_plast[index_interval][4] = self.diameter_saddles_edit.text()
        self.labels_plast[index_interval][5] = self.diameter_ball_edit.text()


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSo(parent), 'Проверка корректности данных перфорации')


class PerforationCorrectGnktFrez(WindowUnion):

    def __init__(self, parent=None):
        super(PerforationCorrectGnktFrez, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна

        self.tabWidget = TabWidget(self.data_well)

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.add_row_table)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)

    def add_row_table(self):
        # Пересохранение данных по интервалам портам
        self.dict_perforation = self.data_well.dict_perforation
        plast_work = list(self.dict_perforation.keys())[0]
        manufacturer = self.tabWidget.currentWidget().manufacturer_combo.currentText()
        type_column = self.tabWidget.currentWidget().type_column_edit.text()

        ports_tuple = sorted(list(self.dict_perforation[plast_work]['интервал']), key=lambda x: x[0], reverse=True)
        dict_ports = {}
        # print(f'порты собрать {ports_tuple}')
        for index, port in enumerate(ports_tuple):
            roof = self.tabWidget.currentWidget().labels_plast[index][1]
            sole = self.tabWidget.currentWidget().labels_plast[index][2]
            type_sanddles = self.tabWidget.currentWidget().labels_plast[index][3]
            ball = self.tabWidget.currentWidget().labels_plast[index][4]
            saddle = self.tabWidget.currentWidget().labels_plast[index][5]

            dict_ports.setdefault(manufacturer, {}).setdefault(type_column, {}).setdefault(f'№{index + 1}',
                                                                                           {}).setdefault(
                'кровля', round(float(roof), 2))
            dict_ports.setdefault(manufacturer, {}).setdefault(type_column, {}).setdefault(
                f'№{index + 1}', {}).setdefault('подошва', round(float(sole), 2))
            dict_ports.setdefault(manufacturer, {}).setdefault(type_column, {}).setdefault(
                f'№{index + 1}', {}).setdefault('шар', ball)
            dict_ports.setdefault(manufacturer, {}).setdefault(type_column, {}).setdefault(
                f'№{index + 1}', {}).setdefault('седло', saddle)
            dict_ports.setdefault(manufacturer, {}).setdefault(type_column, {}).setdefault(
                f'№{index + 1}', {}).setdefault('тип', type_sanddles)
        # print(dict_ports)
        self.dict_ports = dict_ports

        data_list.pause = False
        self.close()
        return dict_ports


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = PerforationCorrectGnktFrez()
    QTimer.singleShot(2000, PerforationCorrectGnktFrez.updateLabel)
    # window.show()
    app.exec_()
