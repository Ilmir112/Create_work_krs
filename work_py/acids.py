from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QGridLayout, QLineEdit, QTabWidget, \
    QMainWindow, QPushButton


import data_list

from work_py.acid_paker import CheckableComboBox
from work_py.alone_oreration import well_volume

from work_py.rationingKRS import liftingNKT_norm, descentNKT_norm
from work_py.parent_work import TabPageUnion, WindowUnion, TabWidgetUnion


class TabPageDp(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.point_bottom_Label = QLabel("глубина нижней точки", self)
        self.point_bottom_edit = QLineEdit(self)

        self.points_sko_Label = QLabel("точки обработки", self)
        self.points_sko_edit = QLineEdit(self)

        plast_work = ['']
        plast_work.extend(self.data_well.plast_work)

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)

        self.acid_label_type = QLabel("Вид кислотной обработки", self)
        self.acid_edit = QComboBox(self)
        self.acid_edit.addItems(['HCl', 'HF', 'ВТ', 'Нефтекислотка'])

        self.acid_volume_label = QLabel("Объем кислотной обработки", self)
        self.acid_volume_edit = QLineEdit(self)

        self.acid_proc_label = QLabel("Концентрация кислоты", self)
        self.acid_proc_edit = QLineEdit(self)
        self.acid_proc_edit.setText('15')
        self.acid_proc_edit.setClearButtonEnabled(True)

        self.acid_calcul_Label = QLabel("объем кислоты на погонный метр", self)
        self.acid_calcul_edit = QLineEdit(self)

        self.iron_label_type = QLabel("необходимость стабилизатора железа", self)
        self.iron_true_combo = QComboBox(self)
        self.iron_true_combo.addItems(['Нет', 'Да'])
        self.iron_volume_label = QLabel("Объем стабилизатора", self)
        self.iron_volume_edit = QLineEdit(self)

        self.pressure_Label = QLabel("Давление закачки", self)
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setClearButtonEnabled(True)
        self.pressure_edit.setText(str(self.data_well.max_admissible_pressure.get_value))

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.plast_label, 2, 1)
        self.grid.addWidget(self.plast_combo, 3, 1)


        self.grid.addWidget(self.points_sko_Label, 2, 2)
        self.grid.addWidget(self.points_sko_edit, 3, 2)

        self.grid.addWidget(self.acid_calcul_Label, 2, 3)
        self.grid.addWidget(self.acid_calcul_edit, 3, 3)

        self.grid.addWidget(self.iron_label_type, 2, 4)
        self.grid.addWidget(self.iron_true_combo, 3, 4)

        self.grid.addWidget(self.iron_volume_label, 2, 5)
        self.grid.addWidget(self.iron_volume_edit, 3, 5)

        self.grid.addWidget(self.acid_label_type, 6, 1)
        self.grid.addWidget(self.acid_edit, 7, 1)

        self.grid.addWidget(self.acid_volume_label, 6, 2)
        self.grid.addWidget(self.acid_volume_edit, 7, 2)

        self.grid.addWidget(self.acid_proc_label, 6, 3)
        self.grid.addWidget(self.acid_proc_edit, 7, 3)

        self.grid.addWidget(self.point_bottom_Label, 6, 4)
        self.grid.addWidget(self.point_bottom_edit, 7, 4)

        self.grid.addWidget(self.pressure_Label, 6, 5)
        self.grid.addWidget(self.pressure_edit, 7, 5)

        self.acid_calcul_edit.textChanged.connect(self.update_volume_points)
        self.points_sko_edit.textChanged.connect(self.update_volume_points)

    def update_volume_points(self):
        acid_calcul = self.acid_calcul_edit.text()
        points_sko = self.points_sko_edit.text()

        if acid_calcul != '':
            acid_calcul = float(acid_calcul)
            if all([char in "0123456789м., " for char in points_sko.replace(' ', '')]):
                bottom_point = max(list(map(int, points_sko.replace('м', '').replace(',', '').split())))
                points_sko = len(points_sko.replace('м', '').replace(',', '.').strip().split('.'))
                self.point_bottom_edit.setText(str(bottom_point))
                volume = round(acid_calcul * float(points_sko),1)
                self.acid_volume_edit.setText(str(volume))


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageDp(parent), 'ГОНС')


class GonsWindow(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)


        self.insert_index = data_well.insert_index
        self.tabWidget = TabWidget(self.data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.dict_perforation = self.data_well.dict_perforation

        self.table_widget = table_widget
        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):

        plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
        acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()
        acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
        acid_proc_edit = int(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.'))
        bottom_point = self.tabWidget.currentWidget().point_bottom_edit.text()
        acid_calcul_edit = self.tabWidget.currentWidget().acid_calcul_edit.text()
        points_sko_edit = self.tabWidget.currentWidget().points_sko_edit.text()
        pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text())
        iron_true_combo = self.tabWidget.currentWidget().iron_true_combo.currentText()
        iron_volume_edit = self.tabWidget.currentWidget().iron_volume_edit.text()

        if int(bottom_point) >= self.data_well.current_bottom:
            QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
            return
        if not acid_edit or not acid_volume_edit or not acid_proc_edit or not bottom_point or not acid_calcul_edit \
                or not points_sko_edit or not pressure_edit:
            QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return

        work_list = self.acidGons(plast_combo, acid_edit, acid_volume_edit, acid_proc_edit, points_sko_edit, bottom_point,
                                  acid_calcul_edit, pressure_edit, iron_true_combo, iron_volume_edit)
        self.populate_row(self.insert_index, work_list, self.table_widget)
        self.calculate_chemistry(acid_edit, acid_volume_edit)
        data_list.pause = False
        self.close()
        return work_list

    def closeEvent(self, event):
                # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия
    def acidGons(self, plast_combo, acid_edit, acid_volume_edit, acid_proc_edit, points_sko_edit, bottom_point,
                                  acid_calcul_edit, pressure_edit, iron_true_combo, iron_volume_edit):
        if iron_true_combo == 'Да':
            iron_str = f' с добавлением стабилизатор железа (Hi-Iron)  из расчета 10кг на 1тн ({iron_volume_edit}кг)'
        else:
            iron_str = ""

        nkt_combo = f' + НКТ60мм {round(self.data_well.current_bottom -self.data_well.head_column_additional.get_value, 0)}' \
            if self.data_well.column_additional is True else ''
        gons_list = [[f'Спуск гидромониторную насадку yf {nkt_combo} до глубины нижней точки до {bottom_point}', None,
         f'Спустить  гидромониторную насадку {nkt_combo}'         
         f'на НКТ{self.data_well.nkt_diam}мм до глубины нижней точки до {bottom_point}'
         f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм.',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(bottom_point,1)],
         [f' ГОНС пласта {plast_combo} (общий объем {acid_volume_edit}м3) в инт. {points_sko_edit}м', None,
          f'Провести ОПЗ пласта {plast_combo} силами СК Крезол по технологии ГОНС в инт. {points_sko_edit} '
          f'с закачкой {acid_edit} '
          f'{acid_proc_edit}% в объеме по {acid_calcul_edit}м3/точке (общий объем {acid_volume_edit}м3) при давлении '
          f'не более {pressure_edit}атм{iron_str} в присутствии '
          f'представителя сектора супервайзерского контроля за текущим и капитальным ремонтом скважин (ГОНС произвести '
          f'снизу-вверх).',
          None, None, None, None, None, None, None,
          'мастер КРС', 8],
         [None, None,
          f'По согласованию с заказчиком  допустить компоновку до глубины {self.data_well.current_bottom}м, промыть скважину '
          f'прямой промывкой через желобную ёмкость водой у= {self.data_well.fluid_work} в присутствии представителя заказчика в '
          f'объеме {round(well_volume(self, self.data_well.current_bottom), 1)}м3. Промывку производить в емкость '
          f'для дальнейшей утилизации на НШУ с целью недопущения попадания кислоты в систему сбора.',
          None, None, None, None, None, None, None,
          'мастер КРС', 1.2],
         [None, None,
          f'Поднять гидромониторную насадку на НКТ{self.data_well.nkt_diam}мм c глубины {self.data_well.current_bottom}м с '
          f'доливом скважины в '
          f'объеме {round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 удельным весом {self.data_well.fluid_work}',
          None, None, None, None, None, None, None,
          'мастер КРС',
          liftingNKT_norm(self.data_well.current_bottom, 1)]]

        return gons_list