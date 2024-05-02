from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QGridLayout, QLineEdit, QTabWidget, \
    QMainWindow, QPushButton

import krs
import well_data
from gnkt_data.gnkt_data import gnkt_dict
from main import MyWindow
from .acid_paker import CheckableComboBox
from .alone_oreration import well_volume

from .rationingKRS import liftingNKT_norm, descentNKT_norm

class TabPageDp(QWidget):
    def __init__(self):
        super().__init__()

        self.point_bottom_Label = QLabel("глубина нижней точки", self)
        self.point_bottom_edit = QLineEdit(self)

        self.poins_sko_Label = QLabel("точки обработки", self)
        self.poins_sko_edit = QLineEdit(self)


        plast_work = ['']
        plast_work.extend(well_data.plast_work)

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
        self.acid_calcul_Edit = QLineEdit(self)

        self.iron_label_type = QLabel("необходимость стабилизатора железа", self)
        self.iron_true_combo = QComboBox(self)
        self.iron_true_combo.addItems(['Нет', 'Да'])
        self.iron_volume_label = QLabel("Объем стабилизатора", self)
        self.iron_volume_edit = QLineEdit(self)

        self.pressure_Label = QLabel("Давление закачки", self)
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setClearButtonEnabled(True)
        self.pressure_edit.setText(str(well_data.max_admissible_pressure._value))

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.plast_label, 2, 1)
        self.grid.addWidget(self.plast_combo, 3, 1)


        self.grid.addWidget(self.poins_sko_Label, 2, 2)
        self.grid.addWidget(self.poins_sko_edit, 3, 2)

        self.grid.addWidget(self.acid_calcul_Label, 2, 3)
        self.grid.addWidget(self.acid_calcul_Edit, 3, 3)



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

        self.acid_calcul_Edit.textChanged.connect(self.update_volume_points)
        self.poins_sko_edit.textChanged.connect(self.update_volume_points)

    def update_volume_points(self):
        acid_calcul = self.acid_calcul_Edit.text()
        poins_sko = self.poins_sko_edit.text()

        if acid_calcul != '':
            acid_calcul = float(acid_calcul)
            if all([char in "0123456789м., " for char in poins_sko.replace(' ', '')]):
                bottom_point = max(list(map(int, poins_sko.replace('м', '').replace(',', '').split())))
                poins_sko = len(poins_sko.replace('м', '').replace(',', '.').strip().split('.'))
                self.point_bottom_edit.setText(str(bottom_point))
                volume = round(acid_calcul * float(poins_sko),1)
                self.acid_volume_edit.setText(str(volume))


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPageDp(), 'ГОНС')


class GonsWindow(QMainWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.tabWidget = TabWidget()
        self.dict_perforation = well_data.dict_perforation
        self.ins_ind = ins_ind
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
        acid_calcul_Edit = self.tabWidget.currentWidget().acid_calcul_Edit.text()
        poins_sko_edit = self.tabWidget.currentWidget().poins_sko_edit.text()
        pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text())
        iron_true_combo = self.tabWidget.currentWidget().iron_true_combo.currentText()
        iron_volume_edit = self.tabWidget.currentWidget().iron_volume_edit.text()

        if int(bottom_point) >= well_data.current_bottom:
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
            return
        if not acid_edit or not acid_volume_edit or not acid_proc_edit or not bottom_point or not acid_calcul_Edit \
                or not poins_sko_edit or not pressure_edit:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return

        work_list = self.acidGons(plast_combo, acid_edit, acid_volume_edit, acid_proc_edit, poins_sko_edit, bottom_point,
                                  acid_calcul_Edit, pressure_edit, iron_true_combo, iron_volume_edit)
        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()
        return work_list
    def acidGons(self, plast_combo, acid_edit, acid_volume_edit, acid_proc_edit, poins_sko_edit, bottom_point,
                                  acid_calcul_Edit, pressure_edit, iron_true_combo, iron_volume_edit):
        if iron_true_combo == 'Да':
            iron_str = f' с добавлением стабилизатор железа (Hi-Iron)  из расчета 10кг на 1тн ({iron_volume_edit}кг)'
        else:
            iron_str = ""

        nkt_combo = f" + НКТ60мм {round(well_data.current_bottom -well_data.head_column_additional._value, 0)}" \
            if well_data.column_additional is True else ""
        gons_list = [[f'Спуск гидромониторную насадку yf {nkt_combo} до глубины нижней точки до {bottom_point}', None,
         f'Спустить  гидромониторную насадку {nkt_combo}'         
         f'на НКТ{well_data.nkt_diam}мм до глубины нижней точки до {bottom_point}'
         f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(bottom_point,1)],
         [f' ГОНС пласта {plast_combo} (общий объем {acid_volume_edit}м3) в инт. {poins_sko_edit}м', None,
          f'Провести ОПЗ пласта {plast_combo} силами СК Крезол по технологии ГОНС в инт. {poins_sko_edit} '
          f'с закачкой {acid_edit} '
          f'{acid_proc_edit}% в объеме по {acid_calcul_Edit}м3/точке (общий объем {acid_volume_edit}м3) при давлении '
          f'не более {pressure_edit}атм{iron_str} в присутствии '
          f'представителя сектора супервайзерского контроля за текущим и капитальным ремонтом скважин (ГОНС произвести '
          f'снизу-вверх).',
          None, None, None, None, None, None, None,
          'мастер КРС', 8],
         [None, None,
          f'По согласованию с заказчиком  допустить компоновку до глубины {well_data.current_bottom}м, промыть скважину '
          f'прямой промывкой через желобную ёмкость водой у= {well_data.fluid_work} в присутствии представителя заказчика в '
          f'объеме {round(well_volume(self, well_data.current_bottom), 1)}м3. Промывку производить в емкость '
          f'для дальнейшей утилизации на НШУ с целью недопущения попадания кислоты в систему сбора.',
          None, None, None, None, None, None, None,
          'мастер КРС', 1.2],
         [None, None,
          f'Поднять гидромониторную насадку на НКТ{well_data.nkt_diam}мм c глубины {well_data.current_bottom}м с '
          f'доливом скважины в '
          f'объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
          None, None, None, None, None, None, None,
          'мастер КРС',
          liftingNKT_norm(well_data.current_bottom, 1)]]

        return gons_list