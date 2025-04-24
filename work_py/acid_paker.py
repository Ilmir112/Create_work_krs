from PyQt5 import QtWidgets

from PyQt5.Qt import QWidget, QLabel, QComboBox, QGridLayout, QPushButton
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QPalette, QStandardItem, QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QStyledItemDelegate, qApp, QMessageBox, QCompleter, QTableWidget, \
    QTableWidgetItem, QLineEdit

import data_list
from work_py.alone_oreration import kot_work
from work_py.parent_work import TabPageUnion, WindowUnion, TabWidgetUnion
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm
from work_py.swabbing import SwabWindow


class CheckableComboBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.combo_box = CheckableComboBoxChild(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.combo_box)


class CheckableComboBoxChild(QComboBox):
    # Subclass Delegate to increase item height

    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.lineEdit().setPlaceholderText("--выбрать пласты--")
        edit = self.lineEdit()
        self.setLineEdit(edit)
        self.completer = QCompleter()
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        edit.setCompleter(self.completer)
        self.completer.setModel(self.model())
        edit.returnPressed.connect(self.insertCustomItem)

        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBoxChild.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):
        try:
            if object == self.view().viewport():
                if event.type() == QEvent.MouseButtonRelease:
                    if self.lineEdit().hasFocus():
                        return True
                    index = self.view().indexAt(event.pos())
                    item = self.model().item(index.row())
                    if item.checkState() == Qt.Checked:
                        item.setCheckState(Qt.Unchecked)
                    else:
                        item.setCheckState(Qt.Checked)
                    return False
            return False
        except Exception:
            pass

    def timerEvent(self, event):

        self.killTimer(event.timerId())

    def updateText(self):
        data_list.texts = []

        for i in range(self.model().rowCount()):

            if self.model().item(i).checkState() == Qt.Checked:
                # print(self.model().item(i).text())

                data_list.texts.append(self.model().item(i).text())

        text = ", ".join(data_list.texts)

        self.lineEdit().setText(text)

    def addItem(self, text, data=None, checked=False):
        from category_correct import TabPageSo

        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

        if text in data_list.plast_work and not text in TabPageSo.count_plast:
            if text not in TabPageSo.count_plast:
                item.setData(Qt.Unchecked if not text in data_list.plast_work else Qt.Checked, Qt.CheckStateRole)
                TabPageSo.count_plast.append(text)
        else:
            if data_list.plast_project:
                if text not in TabPageSo.count_plast:
                    item.setData(Qt.Unchecked if not text in data_list.plast_project else Qt.Checked, Qt.CheckStateRole)

        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def insertCustomItem(self):
        text = self.lineEdit().text().strip()
        # Split the text by comma, and lowercase and strip() each piece
        typedItemsOriginal = [item.strip() for item in text.split(",") if item.strip()]
        typedItemsLower = [item.lower() for item in typedItemsOriginal]
        # Uncheck all items
        for i in range(self.model().rowCount()):
            self.model().item(i).setData(Qt.Unchecked, Qt.CheckStateRole)
        # Loop through each item in the text and check it, if it exists in
        # lowercase
        for i in range(len(typedItemsOriginal)):
            for j in range(self.model().rowCount()):
                if self.model().item(j).text().lower() == typedItemsLower[i]:
                    self.model().item(j).setData(Qt.Checked, Qt.CheckStateRole)
                    break
            else:
                # If the item doesn't exist, add it to the list
                self.addItem(typedItemsOriginal[i], checked=True)
        self.updateText()
        self.showPopup()

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res


class TabPageSoAcid(TabPageUnion):
    def __init__(self, tableWidget, parent=None):
        super().__init__(parent)

        self.data_well = parent
        self.distance_between_packers_voronka = None
        self.distance_between_packers = None

        self.tableWidget = tableWidget

        self.validator_int = QIntValidator(0, 8000)

        self.paker_layout_label = QLabel("Компоновка пакеров", self)
        self.paker_layout_combo = QComboBox(self)
        paker_layout_list = ['воронка', 'однопакерная', 'двухпакерная',
                             'однопакерная, упорный', 'двухпакерная, упорные', 'пакер с заглушкой',
                             'без монтажа компоновки на спуск']
        self.paker_layout_combo.addItems(paker_layout_list)

        self.depth_gauge_label = QLabel("глубинные манометры", self)
        self.depth_gauge_combo = QComboBox(self)
        self.depth_gauge_combo.addItems(['Нет', 'Да'])
        self.depth_gauge_combo.setProperty("value", "Нет")

        self.diameter_paker_label_type = QLabel("Диаметр пакера", self)
        self.diameter_paker_edit = QLineEdit(self)

        self.kvost_label = QLabel("Длина хвостовики", self)
        self.paker_khost = QLineEdit(self)

        self.pakerLabel = QLabel("глубина пакера", self)
        self.paker_depth_edit = QLineEdit(self)

        self.paker2Label = QLabel("глубина верхнего пакера", self)
        self.paker2_depth = QLineEdit(self)
        if self.data_well:
            self.paker2_depth.setText(f'{int(self.data_well.perforation_roof - 20)}')

        self.need_privyazka_Label = QLabel("Привязка оборудования", self)
        self.need_privyazka_q_combo = QComboBox()
        self.need_privyazka_q_combo.addItems(['Нет', 'Да'])

        plast_work = ['']
        if self.data_well:
            plast_work.extend(self.data_well.plast_work)

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)

        self.skv_true_label_type = QLabel("необходимость кислотной ванны", self)
        self.svk_true_combo = QComboBox(self)
        self.svk_true_combo.addItems(['без СКВ', 'Нужно СКВ', ])

        self.sko_true_label_type = QLabel("необходимость СКО", self)
        self.sko_true_combo = QComboBox(self)
        self.sko_true_combo.addItems(['Нет', 'Да'])

        self.paker_depth_zumpf_label = QLabel("Глубина посадки для ЗУМПФа", self)
        self.paker_depth_zumpf_edit = QLineEdit(self)
        self.paker_depth_zumpf_edit.setValidator(self.validator_int)

        self.pressure_zumpf_question_label = QLabel("Нужно ли опрессовывать ЗУМПФ", self)
        self.pressure_zumpf_question_combo = QComboBox(self)
        self.pressure_zumpf_question_combo.addItems(["Нет", "Да"])

        self.pressure_Label = QLabel("Давление закачки", self)
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setClearButtonEnabled(True)

        self.grid.addWidget(self.pressure_Label, 6, 6)
        self.grid.addWidget(self.pressure_edit, 7, 6)

        self.grid.addWidget(self.paker_layout_label, 0, 0, 1, 0)
        self.grid.addWidget(self.paker_layout_combo, 1, 0, 1, 0)
        self.swab_true_label_type = QLabel("необходимость освоения", self)
        self.swab_true_edit_type = QComboBox(self)

        self.swab_true_edit_type.addItems(['без освоения', 'Нужно освоение'])

        self.grid.addWidget(self.swab_true_label_type, 12, 0)
        self.grid.addWidget(self.swab_true_edit_type, 13, 0)

        self.grid.addWidget(self.plast_label, 2, 1)
        self.grid.addWidget(self.plast_combo, 3, 1)
        self.grid.addWidget(self.depth_gauge_label, 2, 2)
        self.grid.addWidget(self.depth_gauge_combo, 3, 2)
        self.grid.addWidget(self.diameter_paker_label_type, 2, 3)
        self.grid.addWidget(self.diameter_paker_edit, 3, 3)
        self.grid.addWidget(self.kvost_label, 2, 4)
        self.grid.addWidget(self.paker_khost, 3, 4)
        self.grid.addWidget(self.pakerLabel, 2, 5)
        self.grid.addWidget(self.paker_depth_edit, 3, 5)
        self.grid.addWidget(self.paker2Label, 2, 6)
        self.grid.addWidget(self.paker2_depth, 3, 6)
        self.grid.addWidget(self.need_privyazka_Label, 2, 7)
        self.grid.addWidget(self.need_privyazka_q_combo, 3, 7)

        self.grid.addWidget(self.pressure_zumpf_question_label, 2, 8)
        self.grid.addWidget(self.pressure_zumpf_question_combo, 3, 8)
        self.grid.addWidget(self.paker_depth_zumpf_label, 2, 9)
        self.grid.addWidget(self.paker_depth_zumpf_edit, 3, 9)
        self.grid.addWidget(self.sko_true_label_type, 6, 0)
        self.grid.addWidget(self.sko_true_combo, 7, 0)
        self.grid.addWidget(self.skv_true_label_type, 4, 0)
        self.grid.addWidget(self.svk_true_combo, 5, 0)

        self.paker_depth_edit.textChanged.connect(self.update_paker_depth)
        self.paker_depth_edit.textChanged.connect(self.update_paker_edit)
        self.paker2_depth.textChanged.connect(self.update_paker_edit)

        self.sko_true_combo.currentTextChanged.connect(self.update_sko_true)

        self.svk_true_combo.currentTextChanged.connect(self.update_skv_edit)

        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_paker_edit)

        self.pressure_zumpf_question_combo.currentTextChanged.connect(self.update_paker_need)
        self.pressure_zumpf_question_combo.setCurrentIndex(1)
        self.pressure_zumpf_question_combo.setCurrentIndex(0)
        self.swab_true_edit_type.currentTextChanged.connect(self.update_need_swab)
        self.swab_true_edit_type.setCurrentIndex(1)
        self.swab_true_edit_type.setCurrentIndex(0)
        self.sko_true_combo.setCurrentIndex(1)

    def update_paker_need(self, index):
        if index == 'Да' and self.data_well:
            paker_depth_zumpf = int(self.data_well.perforation_roof + 10)
            if len(self.data_well.plast_work) != 0:
                paker_depth_zumpf = int(self.data_well.perforation_roof + 10)
            else:
                if self.data_well.dict_leakiness:
                    paker_depth_zumpf = int(max([float(nek.split('-')[0]) + 10
                                                 for nek in self.data_well.dict_leakiness['НЭК']['интервал'].keys()]))

            self.paker_depth_zumpf_edit.setText(f'{paker_depth_zumpf}')

            self.grid.addWidget(self.paker_depth_zumpf_label, 2, 9)
            self.grid.addWidget(self.paker_depth_zumpf_edit, 3, 9)
        elif index == 'Нет':
            self.paker_depth_zumpf_label.setParent(None)
            self.paker_depth_zumpf_edit.setParent(None)

    def update_paker_depth(self):
        paker_depth = self.paker_depth_edit.text()
        if paker_depth:
            paker_diameter = int(float(self.paker_diameter_select(paker_depth)))
            self.diameter_paker_edit.setText(str(paker_diameter))
        if self.data_well:
            self.pressure_edit.setText(str(self.data_well.max_admissible_pressure.get_value))

    def update_paker_layout(self, index):
        self.paker_layout_index = index

        if index not in ['однопакерная']:
            self.pressure_zumpf_question_label.setParent(None)
            self.pressure_zumpf_question_combo.setParent(None)
        else:
            self.grid.addWidget(self.pressure_zumpf_question_label, 2, 8)
            self.grid.addWidget(self.pressure_zumpf_question_combo, 3, 8)

        if index in ['однопакерная', 'пакер с заглушкой', 'однопакерная, упорный', ]:
            paker_layout_list_tab = ["Пласт", "хвост", "пакер", "СКВ", "вид кислоты", "процент", "объем", "объем нефти"]
            self.grid.addWidget(self.pakerLabel, 2, 5)
            self.grid.addWidget(self.paker_depth_edit, 3, 5)
            self.paker2Label.setParent(None)
            self.paker2_depth.setParent(None)

            if index == 'однопакерная, упорный' or 'пакер с заглушкой' == index:
                paker_depth = self.paker_depth_edit.text()
                if paker_depth != '':
                    self.paker_khost.setText(f'{int(self.data_well.current_bottom - int(paker_depth))}')
        elif index in ['двухпакерная', 'двухпакерная, упорные']:
            paker_layout_list_tab = ["Пласт", "хвост", "пакер нижний", 'пакер вверхний', "СКВ",
                                     "вид кислоты", "процент", "объем", "объем нефти"]
            self.grid.addWidget(self.paker2Label, 2, 6)
            self.grid.addWidget(self.paker2_depth, 3, 6)
            self.grid.addWidget(self.pakerLabel, 2, 5)
            self.grid.addWidget(self.paker_depth_edit, 3, 5)
            if index == 'двухпакерная, упорные':
                paker_depth = self.paker_depth_edit.text()
                if paker_depth != '':
                    self.paker_khost.setText(f'{int(self.data_well.current_bottom - int(paker_depth))}')
        elif index in ['воронка', 'без монтажа компоновки на спуск']:
            if self.data_well:
                paker_layout_list_tab = ["Пласт", "воронка", "СКВ",
                                         "вид кислоты", "процент", "объем", "объем нефти"]
                self.paker_khost.setText(f'{int(self.data_well.perforation_sole)}')
                self.paker2Label.setParent(None)
                self.paker2_depth.setParent(None)
                self.pakerLabel.setParent(None)
                self.paker_depth_edit.setParent(None)
        elif index in ['ГОНС']:
            paker_layout_list_tab = ["Пласт", "точки", "пом.",
                                     "вид кислоты", "процент", "объем"]
        self.tableWidget.setHorizontalHeaderLabels(paker_layout_list_tab)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

    def update_plast_edit(self):
        if self.data_well:
            dict_perforation = self.data_well.dict_perforation
            plasts = data_list.texts
            # print(f'пласты {plasts, len(data_list.texts), len(plasts), data_list.texts}')
            roof_plast = self.data_well.current_bottom
            sole_plast = 0
            for plast in self.data_well.plast_work:
                for plast_sel in plasts:
                    if plast_sel == plast:

                        if roof_plast >= dict_perforation[plast]['кровля']:
                            roof_plast = dict_perforation[plast]['кровля']
                        if sole_plast <= dict_perforation[plast]['подошва']:
                            sole_plast = dict_perforation[plast]['подошва']

            if self.paker_layout_combo.currentText() == 'однопакерная':
                paker_depth = int(roof_plast - 20)
                self.paker_depth_edit.setText(f"{paker_depth}")

                if paker_depth != '':
                    self.paker_khost.setText(str(int(sole_plast - paker_depth)))
                    self.swab_paker_depth.setText(str(int(roof_plast - 40 - int(float(self.paker_khost.text())))))
            elif self.paker_layout_combo.currentText() in ['однопакерная, упорный', 'пакер с заглушкой']:

                paker_depth = int(roof_plast - 20)
                self.paker_depth_edit.setText(f"{paker_depth}")
                if paker_depth != '':
                    self.paker_khost.setText(str(int(self.data_well.current_bottom - paker_depth)))
                    self.swab_paker_depth.setText(f'{paker_depth}')
            elif self.paker_layout_combo.currentText() in ['двухпакерная']:
                paker_depth = int(sole_plast + 10)
                if paker_depth != '':
                    if paker_depth + 10 >= self.data_well.current_bottom:
                        self.paker_khost.setText(f"{10}")
                    else:
                        self.paker_khost.setText(f"{1}")
                    self.paker_depth_edit.setText(f"{paker_depth}")
                    self.paker2_depth.setText(f"{int(roof_plast - 10)}")
                    self.swab_paker_depth.setText(str(paker_depth))
            elif self.paker_layout_combo.currentText() == 'двухпакерная, упорные':
                paker_depth = int(sole_plast + 10)
                if paker_depth != '':
                    self.paker_khost.setText(f'{self.data_well.current_bottom - paker_depth}')
                    self.paker_depth_edit.setText(f"{paker_depth}")
                    self.paker2_depth.setText(f"{int(roof_plast - 10)}")
                    self.swab_paker_depth.setText(str(paker_depth))
            elif self.paker_layout_combo.currentText() == 'без монтажа компоновки на спуск':
                self.paker_khost.setText(f'')
                self.paker_depth_edit.setText(f'')
                self.paker2_depth.setText(f'')
                self.swab_paker_depth.setText(f'')

            # print(f'кровля {roof_plast}, подошва {sole_plast}')

    def update_paker_edit(self):
        if self.data_well:
            dict_perforation = self.data_well.dict_perforation
            rows = self.tableWidget.rowCount()
            plasts = data_list.texts
            # print(plasts)
            roof_plast = self.data_well.current_bottom
            sole_plast = 0
            for plast in self.data_well.plast_work:
                for plast_sel in plasts:
                    if plast_sel == plast:
                        if roof_plast >= dict_perforation[plast]['кровля']:
                            roof_plast = dict_perforation[plast]['кровля']
                        if sole_plast <= dict_perforation[plast]['подошва']:
                            sole_plast = dict_perforation[plast]['подошва']
            paker_depth = self.paker_depth_edit.text()

            if self.paker_layout_combo.currentText() in ['однопакерная', 'пакер с заглушкой', 'двухпакерная']:
                if paker_depth != '':
                    paker_depth = float(paker_depth)
                    for plast in self.data_well.dict_perforation:
                        if any(abs(paker_depth - roof) < 10 or abs(paker_depth - sole) < 10
                               for roof, sole in self.data_well.dict_perforation[plast]['интервал']):
                            self.need_privyazka_q_combo.setCurrentIndex(1)

            if self.paker_layout_combo.currentText() in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:

                if paker_depth != '':
                    if self.swab_true_edit_type == 'Нужно освоение':
                        self.swab_paker_depth.setText(f'{roof_plast - (int(sole_plast) - int(paker_depth))}')
                    if self.paker_layout_combo.currentText() in ['однопакерная, упорный', 'пакер с заглушкой']:
                        self.paker_khost.setText(str(int(self.data_well.current_bottom - int(paker_depth))))
                        if self.swab_true_edit_type == 'Нужно освоение':
                            self.swab_paker_depth.setText(f'{paker_depth}')
                if rows == 0:
                    self.paker_khost.setText(str(int(sole_plast - int(paker_depth))))
                    if paker_depth != '' and self.paker_khost.text() != '':
                        self.distance_between_packers_voronka = int(self.paker_khost.text())
                else:
                    if self.paker_khost != '':
                        self.paker_khost.setText(f'{self.distance_between_packers_voronka}')
                    self.paker_khost.setEnabled(False)
            elif self.paker_layout_combo.currentText() in ['двухпакерная', 'двухпакерная, упорные']:
                if paker_depth != '':
                    self.paker_khost.setText(f'{10}')
                    self.swab_paker_depth.setText(f'{paker_depth}')
                    if self.paker_layout_combo.currentText() == 'двухпакерная, упорные':
                        self.paker_khost.setText(str(int(self.data_well.current_bottom - int(paker_depth))))

                if rows == 0:
                    if self.paker_depth_edit.text() != '' and self.paker2_depth.text() != '':
                        self.distance_between_packers = abs(
                            int(self.paker_depth_edit.text()) - int(self.paker2_depth.text()))
                        # print(f' расстояние между пакерами {self.distance_between_packers}')
                else:
                    if self.paker_depth_edit.text() != '':
                        self.paker2_depth.setText(
                            f'{int(self.paker_depth_edit.text()) - self.distance_between_packers}')
                        self.paker2_depth.setEnabled(False)

            elif self.paker_layout_combo.currentText() in ['воронка', 'без монтажа компоновки на спуск']:
                self.paker_khost.setText(f'{sole_plast}')
                self.swab_paker_depth.setText(f'{roof_plast - 30}')
                self.diameter_paker_edit.setParent(None)
                self.diameter_paker_label_type.setParent(None)

        # print(f'кровля {roof_plast}, подошва {sole_plast}')


class TabWidget(TabWidgetUnion):
    def __init__(self, tableWidget, parent=None):
        super().__init__()
        self.addTab(TabPageSoAcid(tableWidget, parent), 'Кислотная обработка')


class AcidPakerWindow(WindowUnion):

    def __init__(self, data_well=None, table_widget=None, parent=None):
        super().__init__(data_well)

        self.expected_pickup = None
        self.data_well = data_well
        if self.data_well:
            self.insert_index = data_well.insert_index

        self.setWindowFlags(Qt.WindowFlags(Qt.WindowModal))
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.paker_select = None
        self.dict_nkt = {}
        self.work_window = None
        self.sko_volume_all = 0
        self.le = QLineEdit()

        self.table_widget = table_widget
        self.tableWidget = QTableWidget(0, 8)
        self.tab_widget = TabWidget(self.tableWidget, self.data_well)

        if self.data_well:

            if all([self.data_well.dict_perforation[plast]['отрайбировано'] for plast in self.data_well.plast_work]):
                self.tableWidget.setHorizontalHeaderLabels(
                    ["Пласт", "хвост", "пакер", "пакер", "СКВ", "вид кислоты", "процент", "объем", "объем нефти"])
            else:

                self.tableWidget.setHorizontalHeaderLabels(
                    ["Пласт", "хвост", "пакер", "СКВ", "вид кислоты", "процент", "объем", "объем нефти"])

        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonadd_string = QPushButton('Добавить обработку')
        self.buttonadd_string.clicked.connect(self.add_string)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonadd_string, 2, 0)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)

        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0, 1, 0)

        self.mtg_count = None

    def add_string(self):
        self.current_widget = self.tab_widget.currentWidget()
        self.paker_layout_combo = self.current_widget.paker_layout_combo.currentText()
        self.plast_combo = self.current_widget.plast_combo.combo_box.currentText()

        acid_edit_list = ['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка']
        self.acid_edit = self.current_widget.acid_edit.currentText()
        self.acid_combo = QComboBox(self)
        self.acid_combo.addItems(acid_edit_list)
        self.acid_combo.setCurrentIndex(acid_edit_list.index(self.acid_edit))

        self.acid_volume_edit = float(self.current_widget.acid_volume_edit.text().replace(',', '.'))
        self.acid_proc_edit = int(self.current_widget.acid_proc_edit.text().replace(',', '.'))
        self.svk_true_combo_str = str(self.current_widget.svk_true_combo.currentText())
        self.acid_oil_proc_edit = self.current_widget.acid_oil_proc_edit.text()

        self.svk_true_combo = QComboBox(self)
        svk_true_list = ['Нужно СКВ', 'без СКВ']
        self.svk_true_combo.addItems(svk_true_list)
        self.svk_true_combo.setCurrentIndex(svk_true_list.index(self.svk_true_combo_str))

        if not self.plast_combo or not self.acid_edit or not self.acid_volume_edit or not self.acid_proc_edit:
            QMessageBox.information(self, 'Внимание', 'Заполните данные по объему')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()

        if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
            paker_khost = self.check_if_none(self.current_widget.paker_khost.text())
            paker_depth = self.check_if_none(self.current_widget.paker_depth_edit.text())
            if self.data_well:
                if self.data_well.current_bottom < float(paker_khost + paker_depth) or \
                        0 < paker_khost + paker_depth < self.data_well.current_bottom is False:
                    QMessageBox.information(self, 'Внимание',
                                            f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                            f'{self.data_well.current_bottom}м')
                    return
                if self.check_true_depth_template(paker_depth) is False:
                    return
                if self.check_depth_paker_in_perforation(paker_depth) is False:
                    return
                if self.check_depth_in_skm_interval(paker_depth) is False:
                    return

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(self.plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setCellWidget(rows, 3, self.svk_true_combo)
            self.tableWidget.setCellWidget(rows, 4, self.acid_combo)
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(self.acid_proc_edit)))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(self.acid_volume_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(self.acid_oil_proc_edit)))

            self.tableWidget.setSortingEnabled(False)
        elif self.paker_layout_combo in ['двухпакерная', 'двухпакерная, упорные']:
            self.paker_khost = self.check_if_none((self.current_widget.paker_khost.text()))
            self.paker_depth = int(self.check_if_none(self.current_widget.paker_depth_edit.text()))
            self.paker2_depth = int(self.check_if_none(self.current_widget.paker2_depth.text()))

            if self.data_well.current_bottom < float(self.paker_khost + self.paker_depth) or \
                    0 < self.paker_khost + self.paker_depth < self.data_well.current_bottom is False:
                QMessageBox.information(self, 'Внимание',
                                        f'Компоновка ниже {self.paker_khost + self.paker_depth}м текущего забоя '
                                        f'{self.data_well.current_bottom}м')
                return

            if self.data_well:
                if self.check_true_depth_template(self.paker_depth) is False:
                    return
                if self.check_depth_paker_in_perforation(self.paker_depth) is False:
                    return
                if self.check_depth_in_skm_interval(self.paker_depth) is False:
                    return
                if self.check_true_depth_template(self.paker2_depth) is False:
                    return
                if self.check_depth_paker_in_perforation(self.paker2_depth) is False:
                    return
                if self.check_depth_in_skm_interval(self.paker2_depth) is False:
                    return
                if self.data_well.current_bottom < float(self.paker_khost + self.paker2_depth):
                    QMessageBox.information(self, 'Внимание',
                                            f'Компоновка ниже {self.paker_khost + self.paker_depth}м текущего забоя '
                                            f'{self.data_well.current_bottom}м')
                    return
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(self.plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(self.paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(self.paker_depth)))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(self.paker2_depth)))
            self.tableWidget.setCellWidget(rows, 4, self.svk_true_combo)
            self.tableWidget.setCellWidget(rows, 5, self.acid_combo)
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(self.acid_proc_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(self.acid_volume_edit)))
        elif self.paker_layout_combo in ['воронка', 'без монтажа компоновки на спуск']:
            self.paker_depth = int(self.check_if_none(self.current_widget.paker_depth_edit.text()))
            self.paker_khost = self.check_if_none((self.current_widget.paker_khost.text()))
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(self.plast_combo))
            if self.paker_layout_combo in ['воронка']:
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(self.paker_khost)))
            elif self.paker_layout_combo in ['без монтажа компоновки на спуск']:
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(self.paker_khost)))
            self.tableWidget.setCellWidget(rows, 2, self.svk_true_combo)
            self.tableWidget.setCellWidget(rows, 3, self.acid_combo)
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(self.acid_proc_edit)))
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(self.acid_volume_edit)))

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def add_work(self):
        self.current_widget = self.tab_widget.currentWidget()
        try:
            self.need_privyazka_q_combo = self.current_widget.need_privyazka_q_combo.currentText()
            if self.need_privyazka_q_combo == 'Да':
                mes = QMessageBox.question(self, 'Привязка', 'Расстояние между пакером и ИП меньше 10м. '
                                                             'Нужна привязка корректно ли?')
                if mes == QMessageBox.StandardButton.No:
                    return

            self.paker_layout_combo = str(self.current_widget.paker_layout_combo.currentText())
            self.swab_true_edit_type = self.current_widget.swab_true_edit_type.currentText()
            if self.swab_true_edit_type == "Нужно освоение":
                read_swab = self.read_update_need_swab(self.current_widget)
                if read_swab is False:
                    return
            if self.paker_layout_combo not in ['воронка', 'без монтажа компоновки на спуск']:
                self.diameter_paker = int(float(self.current_widget.diameter_paker_edit.text().replace(',', '.')))
            self.depth_gauge_combo = str(self.current_widget.depth_gauge_combo.currentText())

            self.svk_true_combo = self.current_widget.svk_true_combo.currentText()
            if self.svk_true_combo == 'Нужно СКВ':
                read_skv = self.read_update_skv(self.current_widget)
                if read_skv is False:
                    return

            self.sko_true_combo = str(self.current_widget.sko_true_combo.currentText())
            if self.sko_true_combo == "Да":
                read_sko = self.read_sko_need(self.current_widget)
                if read_sko is False:
                    return

                self.expected_pickup = self.current_widget.expected_pickup_edit.text()
                self.expected_pressure = self.current_widget.expected_pressure_edit.text()
                if self.expected_pressure not in [None, 'None', '', '-', 'атм']:
                    self.expected_pressure = int(float(self.expected_pressure.replace(',', '.')))
                self.pressure_three = self.current_widget.pressure_three_edit.text()

            self.pressure_zumph_combo = self.current_widget.pressure_zumpf_question_combo.currentText()

            if self.pressure_zumph_combo == 'Да':
                self.paker_khost = self.check_if_none(self.current_widget.paker_khost.text())
                self.paker_depth_zumpf = self.current_widget.paker_depth_zumpf_edit.text()

                if self.paker_depth_zumpf == '':
                    QMessageBox.warning(self, 'Ошибка', f'не введены глубина опрессовки ЗУМПФа')
                    return
                else:
                    self.paker_depth_zumpf = int(float(self.paker_depth_zumpf.replace(',', '.')))

                if self.paker_khost + self.paker_depth_zumpf >= self.data_well.current_bottom:
                    QMessageBox.warning(self, 'ОШИБКА', 'Длина хвостовика и пакера ниже текущего забоя')
                    return

                if self.check_true_depth_template(self.paker_depth_zumpf) is False:
                    return
                if self.check_depth_paker_in_perforation(self.paker_depth_zumpf) is False:
                    return
                if self.check_depth_in_skm_interval(self.paker_depth_zumpf) is False:
                    return

            else:
                self.paker_depth_zumpf = 0

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка сохранения данных {type(e).__name__}\n\n{str(e)}')
            return
        work_template_list = []
        self.depth_gauge = ''

        self.need_change_zgs_combo = 'Нет'
        if self.depth_gauge_combo == 'Да':
            self.depth_gauge = 'контейнер с манометром МТГ-25 + '
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
                self.mtg_count = 2
            elif self.paker_layout_combo in ['воронка']:
                self.mtg_count = 1
            else:
                self.mtg_count = 3

            work_template_list = [
                [f'Заявить глубинные манометры', None,
                 f'Подать заявку на завоз глубиныx манометров с контейнером',
                 None, None, None, None, None, None, None, 'мастер КРС', None]]

        rows = self.tableWidget.rowCount()
        if rows == 0 and self.svk_true_combo == 'Нужно СКВ' and self.sko_true_combo == 'Нет':
            mes = QMessageBox.question(self, 'СКВ', 'Нужно произвести только СКВ?')
            if mes == QMessageBox.StandardButton.No:
                return

        elif rows == 0:
            QMessageBox.warning(self, "ВНИМАНИЕ", 'Нужно добавить интервалы обработки')
            return
        if rows == 0:
            self.paker_khost = self.current_widget.paker_khost.text()
            if self.paker_khost not in ['', 0, '0']:
                self.paker_khost = float(self.paker_khost.replace(',', '.'))
            else:
                QMessageBox.warning(self, 'Ошибка', 'Не указано глубина НКТ')
                return

            nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(self.paker_khost,
                                                                       self.swab_true_edit_type)
            if self.data_well.column_additional is False or \
                    (self.data_well.column_additional and
                     self.data_well.head_column_additional.get_value >= self.data_well.current_bottom):
                self.dict_nkt = {nkt_diam: float(self.paker_khost) + float(self.paker_khost)}
            else:
                self.dict_nkt = {
                    nkt_diam: round(self.data_well.head_column_additional.get_value, 0),
                    nkt_pod: int(float(self.paker_khost - self.data_well.head_column_additional.get_value))}

            work_template_list.insert(-2, [f'Определить приемистость при Р-{self.pressure_edit}атм', None,
                                           f'Определить приемистость при Р-{self.pressure_edit}атм '
                                           f'в присутствии представителя заказчика.'
                                           f'при отсутствии приемистости произвести установку '
                                           f'СКВ по согласованию с заказчиком',
                                           None, None, None, None, None, None, None,
                                           'мастер КРС, УСРСиСТ', 1.2])
            work_template_list.extend(self.skv_acid_work())
        else:

            for row in range(rows):
                if self.paker_layout_combo in ['двухпакерная', 'двухпакерная, упорные']:
                    self.plast_combo = self.tableWidget.item(row, 0).text()
                    if row == 0:
                        self.paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                        if self.paker_khost < 0:
                            QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
                            return
                        data_list.paker_khost = self.paker_khost
                    else:
                        self.paker_khost = data_list.paker_khost

                    self.paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                    self.paker2_depth = int(float(self.tableWidget.item(row, 3).text()))
                    self.svk_true_combo = self.tableWidget.cellWidget(row, 4).currentText()
                    self.acid_edit = self.tableWidget.cellWidget(row, 5).currentText()
                    self.acid_proc_edit = int(float(self.tableWidget.item(row, 6).text()))
                    self.acid_volume_edit = round(float(self.tableWidget.item(row, 7).text()), 1)
                    if self.acid_edit == 'HCl':
                        self.sko_volume_all += self.acid_volume_edit
                    try:
                        self.acidOilProc = round(float(self.tableWidget.item(row, 8).text()))
                    except Exception:
                        self.acidOilProc = 0

                    if row == 0:
                        work_template_list = self.paker_layout_two()
                    else:
                        work_template_list.append(
                            [f'установить пакера на глубине {self.paker_depth}/{self.paker2_depth}м',
                             None, f'установить пакера на глубине {self.paker_depth}/{self.paker2_depth}м', None, None,
                             None, None, None, None, None,
                             'мастер КРС', 1.2])
                elif self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный']:
                    self.plast_combo = self.tableWidget.item(row, 0).text()
                    if row == 0:
                        self.paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                        data_list.paker_khost = self.paker_khost
                    else:
                        self.paker_khost = data_list.paker_khost
                    self.paker_depth = int(float(self.tableWidget.item(row, 2).text().replace(',', '.')))
                    self.svk_true_combo = self.tableWidget.cellWidget(row, 3).currentText()
                    self.acid_edit = self.tableWidget.cellWidget(row, 4).currentText().replace(',', '.')
                    self.acid_proc_edit = int(float(self.tableWidget.item(row, 5).text()))
                    self.acid_volume_edit = round(float(self.tableWidget.item(row, 6).text().replace(',', '.')), 1)
                    if self.acid_edit == 'HCl':
                        self.sko_volume_all += self.acid_volume_edit

                    try:
                        self.acidOilProc = round(float(self.tableWidget.item(row, 7).text()))
                    except Exception as e:
                        self.acidOilProc = 0

                    if row == 0:
                        work_template_list = self.paker_layout_one()
                    else:
                        work_template_list.append(
                            [f'установить пакер на глубине {self.paker_depth}, '
                             f'хвост на глубине {self.paker_depth + self.paker_khost}м', None,
                             f'установить пакер на глубине {self.paker_depth}, '
                             f'хвост на глубине {self.paker_depth + self.paker_khost}м', None, None,
                             None, None, None, None, None,
                             'мастер КРС', 1.2])
                elif self.paker_layout_combo in ['пакер с заглушкой']:
                    self.plast_combo = self.tableWidget.item(row, 0).text()
                    if row == 0:
                        self.paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                        data_list.paker_khost = self.paker_khost
                    else:
                        self.paker_khost = data_list.paker_khost
                    self.paker_depth = int(float(self.tableWidget.item(row, 2).text().replace(',', '.')))
                    self.svk_true_combo = self.tableWidget.cellWidget(row, 3).currentText()
                    self.acid_edit = self.tableWidget.cellWidget(row, 4).currentText()
                    self.acid_proc_edit = int(float(self.tableWidget.item(row, 5).text().replace(',', '.')))
                    self.acid_volume_edit = round(float(self.tableWidget.item(row, 6).text().replace(',', '.')), 1)
                    if self.acid_edit == 'HCl':
                        self.sko_volume_all += self.acid_volume_edit

                    try:
                        self.acidOilProc = round(float(self.tableWidget.item(row, 7).text()))
                    except Exception:
                        self.acidOilProc = 0

                    work_template_list = self.paker_layout_one_with_zaglushka()

                elif self.paker_layout_combo in ['воронка', 'без монтажа компоновки на спуск']:

                    self.plast_combo = self.tableWidget.item(row, 0).text()
                    if row == 0:
                        self.paker_khost = int(float(self.tableWidget.item(row, 1).text().replace(',', '.')))
                        data_list.paker_khost = self.paker_khost
                    else:
                        self.paker_khost = data_list.paker_khost

                    self.svk_true_combo = self.tableWidget.cellWidget(row, 2).currentText()
                    self.acid_edit = self.tableWidget.cellWidget(row, 3).currentText()
                    self.acid_volume_edit = round(float(self.tableWidget.item(row, 5).text().replace(',', '.')), 1)
                    self.acid_proc_edit = int(float(self.tableWidget.item(row, 4).text().replace(',', '.')))
                    if self.acid_edit == 'HCl':
                        self.sko_volume_all += self.acid_volume_edit

                    try:
                        self.acidOilProc = round(float(self.tableWidget.item(row, 6).text().replace(',', '.')))
                    except Exception:
                        self.acidOilProc = 0
                    if self.paker_layout_combo == 'воронка':
                        work_template_list = self.voronka_layout()
                    elif self.paker_layout_combo == 'без монтажа компоновки на спуск':
                        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(self.paker_khost,
                                                                                   self.swab_true_edit_type)
                        if self.data_well.column_additional is False or \
                                (self.data_well.column_additional and
                                 self.data_well.head_column_additional.get_value >= self.data_well.current_bottom):
                            self.dict_nkt = {nkt_diam: float(self.paker_khost) + float(self.paker_depth)}
                        else:
                            self.dict_nkt = {
                                nkt_diam: round(self.data_well.head_column_additional.get_value, 0),
                                nkt_pod: int(
                                    float(self.data_well.head_column_additional.get_value - self.paker_khost, 0))}
                        work_template_list = []
                if self.svk_true_combo == 'Нужно СКВ':
                    work_template_list.insert(-2, [f'Определить приемистость при Р-{self.pressure_edit}атм', None,
                                                   f'Определить приемистость при Р-{self.pressure_edit}атм '
                                                   f'в присутствии представителя заказчика.'
                                                   f'при отсутствии приемистости произвести установку '
                                                   f'СКВ по согласованию с заказчиком',
                                                   None, None, None, None, None, None, None,
                                                   'мастер КРС, УСРСиСТ', 1.2])
                    work_template_list.extend(self.skv_acid_work())
                if self.QplastEdit == 'ДА':
                    work_template_list.insert(-2,
                                              [f'Насыщение 5м3.  Q пласт {self.plast_combo} при '
                                               f'Р={self.pressure_three_edit}атм', None,
                                               f'Произвести насыщение скважины до стабилизации давления закачки '
                                               f'не менее 5м3. Опробовать  '
                                               f'пласт {self.plast_combo} на приемистость в трех режимах при '
                                               f'Р={self.pressure_three_edit}атм в присутствии '
                                               f'представителя ЦДНГ. '
                                               f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                                               f'с подтверждением за 2 часа до '
                                               f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {self.expected_pickup}м3/сут '
                                               f'при давлении {self.expected_pressure}атм '
                                               f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                                               None, None, None, None, None, None, None,
                                               'мастер КРС', 0.17 + 0.52 + 0.2 + 0.2 + 0.2])
                if self.sko_true_combo == 'Да':
                    if "двух" in self.paker_layout_combo:
                        if row == 0 and self.data_well.curator != 'ОР' and rows != 1:
                            work_template_list.extend(self.acid_work()[:-1])
                        else:
                            work_template_list.extend(self.acid_work())
                    elif "одно" in self.paker_layout_combo or "заглуш" in self.paker_layout_combo:
                        if row == 0 and self.data_well.curator != 'ОР' and rows != 1:
                            work_template_list.extend(self.acid_work()[:-1])
                        else:
                            work_template_list.extend(self.acid_work())
                    elif "воронка" in self.paker_layout_combo or 'без монтажа компоновки на спуск' in self.paker_layout_combo:
                        work_template_list.extend(self.acid_work())
        if self.sko_volume_all < 13 and self.acid_edit == 'HCl':
            mes = QMessageBox.question(self, 'Увеличение объема кислоты',
                                       'С целью проведения кислоты Крезолом необходимо согласовать '
                                       'увеличение объема кислотной обработки на 13м3')
            if mes == QMessageBox.StandardButton.No:
                return

        if self.swab_true_edit_type == "Нужно освоение":
            try:

                for plast in self.plast_combo.split(','):
                    if plast in self.data_well.plast_work:
                        if abs(self.paker_khost + self.swab_paker_depth - self.data_well.dict_perforation[plast][
                            'кровля']) < 20:
                            mes = QMessageBox.question(self, 'Вопрос',
                                                       f'Расстояние между низом компоновки'
                                                       f' {self.paker_khost + self.swab_paker_depth} '
                                                       f'и кровлей ПВР меньше 20м '
                                                       f'{self.data_well.dict_perforation[plast]["кровля"]},'
                                                       f' Продолжить?')
                            if mes == QMessageBox.StandardButton.No:
                                return
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка сохранения данных {type(e).__name__}\n\n{str(e)}')
                return

            if self.paker_layout_combo in ['однопакерная', 'пакер с заглушкой', 'однопакерная, упорный']:
                if self.check_depth_paker_in_perforation(self.swab_paker_depth) is False:
                    return
                if self.check_depth_in_skm_interval(self.swab_paker_depth) is False:
                    return
                if self.check_true_depth_template(self.swab_paker_depth) is False:
                    return

                swab_work_list = SwabWindow.swabbing_with_paker(self)

                work_template_list.extend(swab_work_list[1:])
            elif self.paker_layout_combo in ['двухпакерная', 'двухпакерная, упорные']:
                self.swab_paker_depth = int(float(self.current_widget.swab_paker_depth.text()))
                if self.check_true_depth_template(self.swab_paker_depth) is False:
                    return
                if self.check_depth_paker_in_perforation(self.swab_paker_depth) is False:
                    return
                if self.check_depth_in_skm_interval(self.swab_paker_depth) is False:
                    return

                self.paker_depth2_swab = self.swab_paker_depth - (self.paker_depth - self.paker2_depth)
                if self.check_true_depth_template(self.paker_depth2_swab) is False:
                    return
                if self.check_depth_paker_in_perforation(self.paker_depth2_swab) is False:
                    return
                if self.check_depth_in_skm_interval(self.paker_depth2_swab) is False:
                    return

                swab_work_list = SwabWindow.swabbing_with_2paker(self)
                work_template_list.extend(swab_work_list[-10:])

            elif self.paker_layout_combo == 'воронка':
                swab_work_list = SwabWindow.swabbing_with_voronka(self)
                work_template_list.append(
                    [f'Поднять до глубины {self.swab_paker_depth}', None,
                     f'Поднять воронку до глубины {self.swab_paker_depth}м',
                     None, None, None, None, None, None, None,
                     'мастер КРС',
                     round(self.data_well.current_bottom / 9.52 * 1.51 / 60 * 1.2 * 1.2 * 1.04 + 0.18 + 0.008
                           * 30 / 9.52 + 0.003 * 30 / 9.52, 2)], )
                work_template_list.extend(swab_work_list[1:])

        else:
            if self.paker_layout_combo != 'без монтажа компоновки на спуск':
                work_template_list.append([None, None,
                                           f'Поднять {self.paker_select} на НКТ{self.data_well.nkt_diam} c глубины '
                                           f'{sum(list(self.dict_nkt.values()))}м с '
                                           f'доливом скважины в '
                                           f'объеме {round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 '
                                           f'удельным весом '
                                           f'{self.data_well.fluid_work}',
                                           None, None, None, None, None, None, None,
                                           'мастер КРС',
                                           lifting_nkt_norm(self.data_well.current_bottom, 1)])
        if self.data_well.region == 'ТГМ' and self.data_well.curator == 'ОР' and self.data_well.dict_pump_ecn == 0:
            work_template_list.extend(kot_work(self, self.data_well.current_bottom))

        self.calculate_chemistry(self.acid_edit, self.acid_volume_edit)
        if self.depth_gauge_combo == 'Да':
            work_template_list.extend([
                [f'вывести глубинные манометры', None, 'Подать заявку на вывоз глубинныx манометров',
                 None, None, None, None, None, None, None, 'мастер КРС', None]])
        if work_template_list:
            self.populate_row(self.insert_index, work_template_list, self.table_widget)
            data_list.pause = False
            self.close()
            self.close_modal_forcefully()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def paker_layout_two(self):

        difference_paker = self.paker_depth - self.paker2_depth

        if 'упорны' in self.paker_layout_combo:
            paker_type = 'ПУ'
        else:
            paker_type = 'ПРО-ЯМО'

        gidroyakor_str = ''
        if self.depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ +'
        else:
            mtg_str = ''

        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(self.paker_depth, self.swab_true_edit_type)

        if (self.data_well.column_additional is False) or \
                (
                        self.data_well.column_additional is True and self.paker_depth < self.data_well.head_column_additional.get_value):
            self.paker_select = f'заглушку + сбивной с ввертышем + {mtg_str} НКТ{nkt_diam}м {self.paker_khost}м ' \
                                f'+ пакер {paker_type}-{self.diameter_paker}мм (либо аналог) ' \
                                f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                                f'{self.data_well.column_wall_thickness.get_value}мм + ' \
                                f' {mtg_str}  щелевой фильтр НКТ{nkt_diam} L-{difference_paker}м ' \
                                f'+ пакер ПУ - {self.diameter_paker} + {mtg_str} НКТ{nkt_diam}мм 20м + ' \
                                f'реперный патрубок'
            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ{nkt_diam}м {self.paker_khost}м  + ' \
                               f'пакер {paker_type}-{self.diameter_paker}мм + щелевой фильтр НКТ {difference_paker}м ' \
                               f' + пакер ПУ - {self.diameter_paker} + НКТ{nkt_diam}мм 20м + репер'
            self.dict_nkt = {nkt_diam: float(self.paker_khost) + float(self.paker_depth)}

        else:
            gidroyakor_str = 'гидроякорь'
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ{nkt_pod}мм {self.paker_khost}м  + ' \
                                f'пакер {paker_type}-' \
                                f'{self.diameter_paker}мм (либо аналог) ' \
                                f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                                f'{self.data_well.column_additional_wall_thickness.get_value}мм + ' \
                                f'щелевой фильтр НКТ{nkt_pod} {difference_paker}м ' \
                                f'+ пакер ПУ - {self.diameter_paker} + НКТ{nkt_pod}мм 20м + репер + НКТ{nkt_pod}' \
                                f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                                f'{gidroyakor_str} {mtg_str}'
            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ{nkt_pod}мм {self.paker_khost}м  + ' \
                               f'пакер {paker_type}-' \
                               f'{self.diameter_paker}мм + щелевой фильтр НКТ{nkt_pod} {difference_paker}м ' \
                               f'+ пакер ПУ - {self.diameter_paker} + НКТ{nkt_pod}мм 20м + репер + НКТ{nkt_pod}' \
                               f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                               f'{gidroyakor_str} {mtg_str}'
            self.dict_nkt = {
                nkt_diam: round(self.data_well.head_column_additional.get_value, 0),
                nkt_pod: int(float(self.paker_depth) + float(self.paker_khost) - round(
                    self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 0))}

        paker_list = [
            [self.paker_short, None,
             f'Спустить {self.paker_select} на НКТ{nkt_diam}мм до '
             f'глубины {self.paker_depth}/{self.paker2_depth}м'
             f' с замером, шаблонированием шаблоном {nkt_template}. '
             f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(self.paker_depth, 1.2)],
            [f'Посадить пакер на Н- {self.paker_depth}/{self.paker2_depth}м', None,
             f'Посадить пакер на глубине {self.paker_depth}/{self.paker2_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.3],
            [self.testing_pressure(self.paker2_depth)[1], None,
             self.testing_pressure(self.paker2_depth)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.83 + 0.58],
            [f'срыв 30мин', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None]]

        if self.need_privyazka_q_combo == 'Да' and self.paker_layout_combo in ['двухпакерная']:
            if self.privyazka_nkt()[0] not in paker_list:
                paker_list.insert(1, self.privyazka_nkt()[0])
        if self.depth_gauge_combo == 'Да':
            paker_list.insert(0, [f'Заявить {self.mtg_count} глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить {self.mtg_count} глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])
        return paker_list

    def paker_layout_one(self):

        if 'упорны' in self.paker_layout_combo:
            paker_type = 'ПУ'
        else:
            paker_type = 'ПРО-ЯМО'
        gidroyakor_str = ''

        if self.depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''
        swab_layout2 = ''
        if (self.swab_true_edit_type == 'без освоения' or paker_type == 'ПУ') and 'Ойл' in data_list.contractor:
            swab_layout = 'Заглушку + щелевой фильтр'
            if paker_type != 'ПУ':
                swab_layout2 = 'сбивной клапан с ввертышем'
        else:
            swab_layout = 'воронку c свабоограничителем'

        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(self.paker_depth, self.swab_true_edit_type)

        if (self.data_well.column_additional is False) or \
                (self.data_well.column_additional is True and self.paker_depth <
                 self.data_well.head_column_additional.get_value):
            self.paker_select = f'{swab_layout} {mtg_str} + НКТ{nkt_diam}мм {self.paker_khost}м + ' \
                                f'пакер {paker_type}-' \
                                f'{self.diameter_paker}мм (либо аналог) ' \
                                f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                                f'{self.data_well.column_wall_thickness.get_value}мм + {swab_layout2}' \
                                f' +НКТ{nkt_diam}мм 10м   {mtg_str} + репер'
            self.paker_short = f'{swab_layout} {mtg_str} + НКТ{nkt_diam}мм {self.paker_khost}м + ' \
                               f'пакер {paker_type}-' \
                               f'{self.diameter_paker}мм + {swab_layout2}+ ' \
                               f'НКТ{nkt_diam}мм 10м  {mtg_str} + репер'
            self.dict_nkt = {nkt_diam: float(self.paker_khost) + float(self.paker_depth)}

        elif self.data_well.column_additional is True and \
                self.paker_depth > self.data_well.head_column_additional.get_value:
            gidroyakor_str = 'гидроякорь'
            self.paker_select = f'{swab_layout} 2" + НКТ{nkt_pod} {float(self.paker_khost)}м + пакер {paker_type}-' \
                                f'{self.diameter_paker}мм (либо аналог) ' \
                                f'для ЭК {float(self.data_well.column_additional_diameter.get_value)}мм х ' \
                                f'{self.data_well.column_additional_wall_thickness.get_value}мм + {swab_layout2} ' \
                                f'НКТ{nkt_pod} 10м + репер + НКТ{nkt_pod}' \
                                f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                                f'{mtg_str}'
            self.paker_short = f'{swab_layout} 2" + НКТ{nkt_pod} {float(self.paker_khost)}м + пакер {paker_type}-' \
                               f'{self.diameter_paker}мм  + {swab_layout2} НКТ{nkt_pod} 10м + репер НКТ{nkt_pod} ' \
                               f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                               f'{mtg_str}'
            self.dict_nkt = {
                nkt_diam: round(self.data_well.head_column_additional.get_value, 0),
                nkt_pod: int(float(self.paker_depth) + float(self.paker_khost) - round(
                    self.data_well.head_column_additional.get_value, 0))}
        if self.pressure_zumph_combo == 'Нет':
            paker_list = [
                [f'СПО {self.paker_short} до глубины {self.paker_depth}м, воронкой до '
                 f'{self.paker_depth + self.paker_khost}м',
                 None, f'Спустить {self.paker_select} + {gidroyakor_str} на НКТ{nkt_diam}мм до глубины '
                       f'{self.paker_depth}м, воронкой до {self.paker_depth + self.paker_khost}м'
                       f' с замером, шаблонированием шаблоном {nkt_template}. '
                       f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(self.paker_depth, 1.2)],
                [f'Посадить пакер на глубине {self.paker_depth}м', None,
                 f'Посадить пакер на глубине {self.paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.5],
                [self.testing_pressure(self.paker_depth)[1], None,
                 self.testing_pressure(self.paker_depth)[0],
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', 0.83 + 0.58],
                [f'срыв 30мин', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести '
                 f'ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]]
        else:
            paker_list = [
                [
                    f' СПО {self.paker_short} до глубины {self.paker_depth}м, воронкой до {self.paker_depth + self.paker_khost}м',
                    None,
                    f'Спустить {self.paker_select} + {gidroyakor_str} на НКТ{nkt_diam}мм до глубины '
                    f'{self.paker_depth}м, воронкой до {self.paker_depth + self.paker_khost}м'
                    f' с замером, шаблонированием шаблоном {nkt_template}. '
                    f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} ',
                    None, None, None, None, None, None, None,
                    'мастер КРС', descentNKT_norm(self.paker_depth, 1.2)],
                [f'Опрессовать ЗУМПФ в инт {self.paker_depth_zumpf} - {self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {self.paker_depth_zumpf} - '
                 f'{self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм в течение 30 минут в '
                 f'присутствии представителя заказчика, '
                 f'составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                 f'с подтверждением за 2 часа до начала работ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.77],
                [f'срыв пакера 30мин + 1ч', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [f'Приподнять и посадить пакер на глубине {self.paker_depth}м',
                 None, f'Приподнять и посадить пакер на глубине {self.paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [self.testing_pressure(self.paker_depth)[1], None,
                 self.testing_pressure(self.paker_depth)[0],
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', 0.67],
                [f'срыв пакера 30мин + 1ч', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком '
                 f'произвести ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]]

        if self.need_privyazka_q_combo == 'Да' and self.paker_layout_combo in ['однопакерная', 'пакер с заглушкой']:
            if self.privyazka_nkt()[0] not in paker_list:
                paker_list.insert(1, self.privyazka_nkt()[0])

        if self.depth_gauge_combo == 'Да':
            paker_list.insert(0, [f'Заявить {self.mtg_count} глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить {self.mtg_count} глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])

        return paker_list

    def paker_layout_one_with_zaglushka(self):

        paker_type = 'ПРО-ЯМО'
        gidroyakor_str = ''

        if self.depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''

        swab_layout = 'Заглушку + сбивной с ввертышем '

        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(self.paker_depth, self.swab_true_edit_type)

        if (self.data_well.column_additional is False) or \
                (
                        self.data_well.column_additional is True and self.paker_depth < self.data_well.head_column_additional.get_value):
            self.paker_select = f'{swab_layout} {mtg_str} + НКТ{nkt_diam}мм {self.paker_khost}м + ' \
                                f'пакер {paker_type}-' \
                                f'{self.diameter_paker}мм (либо аналог) ' \
                                f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                                f'{self.data_well.column_wall_thickness.get_value}мм + ' \
                                f'НКТ{nkt_diam}мм 10м  + щелевой фильтр {mtg_str} + репер'
            self.paker_short = f'{swab_layout} {mtg_str} + НКТ{nkt_diam}мм {self.paker_khost}м + ' \
                               f'пакер {paker_type}-' \
                               f'{self.diameter_paker}мм + ' \
                               f'НКТ{nkt_diam}мм 10м + щелевой фильтр {mtg_str} + репер'
            self.dict_nkt = {nkt_diam: float(self.paker_khost) + float(self.paker_depth)}

        elif self.data_well.column_additional is True and self.paker_depth > self.data_well.head_column_additional.get_value:
            gidroyakor_str = 'гидроякорь'
            self.paker_select = f'{swab_layout} 2" + НКТ{nkt_pod} {float(self.paker_khost)}м + пакер {paker_type}-' \
                                f'{self.diameter_paker}мм (либо аналог) ' \
                                f'для ЭК {float(self.data_well.column_additional_diameter.get_value)}мм х ' \
                                f'{self.data_well.column_additional_wall_thickness.get_value}мм +' \
                                f'НКТ{nkt_pod} 10м + щелевой фильтр + репер + НКТ{nkt_pod}' \
                                f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                                f'{gidroyakor_str} {mtg_str}'
            self.paker_short = f'{swab_layout} 2" + НКТ{nkt_pod} {float(self.paker_khost)}м + пакер {paker_type}-' \
                               f'{self.diameter_paker}мм + НКТ{nkt_pod} 10м + щелевой фильтр ' \
                               f'+ репер НКТ{nkt_pod} ' \
                               f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                               f'{gidroyakor_str} {mtg_str}'
            self.dict_nkt = {
                nkt_diam: round(self.data_well.head_column_additional.get_value, 0),
                nkt_pod: int(float(self.paker_depth) + float(self.paker_khost) - round(
                    self.data_well.head_column_additional.get_value, 0))}

        paker_list = [
            [
                f' СПО {self.paker_short} до глубины {self.paker_depth}м, заглушкой до {self.paker_depth + self.paker_khost}м',
                None,
                f'Спустить {self.paker_select} + {gidroyakor_str} на НКТ{nkt_diam}мм до глубины '
                f'{self.paker_depth}м, заглушкой до {self.paker_depth + self.paker_khost}м'
                f' с замером, шаблонированием шаблоном {nkt_template}. '
                f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} ',
                None, None, None, None, None, None, None,
                'мастер КРС', descentNKT_norm(self.paker_depth, 1.2)],
        ]
        for plast in list(self.data_well.dict_perforation.keys()):
            for interval in self.data_well.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - float(self.data_well.depth_fond_paker_before["after"]))) < 10 or abs(
                        float(interval[0] - float(self.data_well.depth_fond_paker_before["after"]))) < 10:
                    if self.privyazka_nkt()[0] not in paker_list:
                        paker_list.insert(1, self.privyazka_nkt()[0])
        if self.depth_gauge_combo == 'Да':
            paker_list.insert(0, [f'Заявить {self.mtg_count} глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить {self.mtg_count} глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])

        return paker_list

    def voronka_layout(self):

        swab_layout = 'воронку со свабоограничителем'
        if self.depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''

        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(self.paker_khost, self.swab_true_edit_type)

        if (self.data_well.column_additional is False) or \
                (
                        self.data_well.column_additional is True and self.paker_khost < self.data_well.head_column_additional.get_value):
            self.paker_select = f'{swab_layout} НКТ{nkt_diam}мм 10м + репер'
            self.paker_short = f'{swab_layout} НКТ{nkt_diam}мм 10м + репер'

            self.dict_nkt = {nkt_diam: float(self.paker_khost)}

        elif self.data_well.column_additional is True and float(
                self.data_well.column_additional_diameter.get_value) < 110 and \
                self.paker_khost > self.data_well.head_column_additional.get_value:

            self.paker_select = f'{swab_layout} 2" + НКТ{nkt_pod}' \
                                f'{round(self.data_well.head_column_additional.get_value - self.paker_khost, 0)}м ' \
                                f' {mtg_str}'
            self.paker_short = f'{swab_layout} 2" + НКТ{nkt_pod}' \
                               f'{round(self.data_well.head_column_additional.get_value - self.paker_khost, 0)}м ' \
                               f' {mtg_str}'
            self.dict_nkt = {
                nkt_diam: round(self.data_well.head_column_additional.get_value, 0),
                nkt_pod: float(self.paker_khost) - round(
                    self.data_well.head_column_additional.get_value, 0)}
        if self.paker_layout_combo != 'без монтажа компоновки на спуск':
            paker_list = [
                [f' СПО {self.paker_short} до глубины {self.paker_khost}м', None,
                 f'Спустить {self.paker_select} +  на НКТ{nkt_diam}мм до глубины '
                 f'{self.paker_khost}м'
                 f' с замером, шаблонированием шаблоном {nkt_template}. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(self.paker_khost, 1)],
            ]

        if self.depth_gauge_combo == 'Да':
            paker_list.insert(0, [f'Заявить {self.mtg_count} глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить {self.mtg_count} глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])

        return paker_list


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()

    window = AcidPakerWindow()
    window.show()
    sys.exit(app.exec_())
