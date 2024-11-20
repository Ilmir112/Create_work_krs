from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton

import data_list
from main import MyMainWindow
from .alone_oreration import volume_vn_ek
from .parent_work import TabPageUnion, WindowUnion, TabWidgetUnion
from .rir import RirWindow

from .opressovka import OpressovkaEK
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm


class TabPageSoTorpedo(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__()

        self.dict_data_well = parent

        self.roof_torpedo_label = QLabel("Глубина торпедирования", self)
        self.roof_torpedo_edit = QLineEdit(self)
        self.roof_torpedo_edit.setValidator(self.validator_float)

        self.diametr_doloto_ek_label = QLabel('Диаметр долото при строительстве скважины')
        self.diametr_doloto_ek_line = QLineEdit(self)
        self.diametr_doloto_ek_line.setValidator(self.validator_float)

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.roof_torpedo_label, 4, 4)
        self.grid.addWidget(self.roof_torpedo_edit, 5, 4)
        self.grid.addWidget(self.diametr_doloto_ek_label, 4, 5)
        self.grid.addWidget(self.diametr_doloto_ek_line, 5, 5)


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoTorpedo(parent), 'Торпедирование ЭК')


class TorpedoWindow(WindowUnion):
    def __init__(self, dict_data_well, table_widget, parent=None):
        super().__init__()

        self.diametr_doloto_ek = None
        self.roof_torpedo = None
        self.dict_data_well = dict_data_well
        self.ins_ind = dict_data_well['ins_ind']
        self.tabWidget = TabWidget(self.dict_data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        self.roof_torpedo = self.tabWidget.currentWidget().roof_torpedo_edit.text()
        self.diametr_doloto_ek = self.tabWidget.currentWidget().diametr_doloto_ek_line.text()
        if '' in [self.roof_torpedo, self.diametr_doloto_ek]:
            QMessageBox.warning(self, 'Ошибка', 'Не введены все значения')
            return
        self.roof_torpedo = int(float(self.roof_torpedo))
        self.diametr_doloto_ek = float(self.diametr_doloto_ek)

        work_list = self.torpedo_work()
        if work_list:
            self.populate_row(self.ins_ind, work_list, self.table_widget)
            self.dict_data_well["head_column"] = data_list.ProtectedIsDigit(self.roof_torpedo)

            self.dict_data_well["max_admissible_pressure"] = data_list.ProtectedIsDigit(50)
            self.dict_data_well["data_well_dict"]['данные']['диаметр долото при бурении'] = \
                self.diametr_doloto_ek
            self.dict_data_well["data_well_dict"]['данные']['максимальное допустимое давление'] = 50
            self.dict_data_well["diametr_doloto_ek"] = data_list.ProtectedIsDigit(self.diametr_doloto_ek)
            data_list.pause = False
            self.close()

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        self.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def torpedo_work(self):
        work_list = [
            [None, None,
             f'По результатам прихватоопределителя определить глубину торпедирования эксплуатационной колонны.',
             None, None, None, None, None, None, None,
             'Мастер КР', None],
            [f'Торпедирование ЭК на глубине {self.roof_torpedo}',
             None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
                   f'По результатам ПО произвести торпедирование э/колонны в муфтовом соединении при обязательном '
                   f'натяжении э/колонны в присутствии представитель заказчика, составить акт на глубине '
                   f'{self.roof_torpedo}м. '
                   f'В случае невозможности извлечения э/к, предусмотреть работы ГИС (ТДШ), '
                   f'промывку кислотным раствором и повторное торпедирование по согласованию с заказчиком.',
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчик по ГИС', 8],
            [f'Промывка глинистым раствором',
             None, f'При отсутствии хода: \n прокачать глинистый раствор через интервал торпедирования и '
                   f'заболонное пространство для '
                   f'восстановления циркуляции, расходись и извлечь верхнюю часть эксплуатационной колонны.',
             None, None, None, None, None, None, None,
             'мастер КРС', 4]
        ]

        return work_list
