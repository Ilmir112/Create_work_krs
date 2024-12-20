from PyQt5 import QtWidgets

from PyQt5.Qt import QWidget, QLabel, QComboBox, QGridLayout, \
    QInputDialog, QPushButton
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QPalette, QStandardItem, QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QStyledItemDelegate, qApp, QMessageBox, QCompleter, QTableWidget, \
    QTableWidgetItem, QLineEdit

import data_list
from work_py.alone_oreration import volume_vn_nkt, well_volume, kot_work
from work_py.parent_work import TabPageUnion, WindowUnion, TabWidgetUnion
from work_py.rationingKRS import descentNKT_norm, well_volume_norm, liftingNKT_norm
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
        self.distance_between_packers_voronka = None
        self.distance_between_packers = None
        self.le = QLineEdit()
        # self.grid = QGridLayout(self)
        self.tableWidget = tableWidget

        self.validator_int = QIntValidator(0, 8000)

        self.paker_layout_label = QLabel("Компоновка пакеров", self)
        self.paker_layout_combo = QComboBox(self)
        paker_layout_list = ['воронка', 'однопакерная', 'двухпакерная',
                             'однопакерная, упорный', 'двухпакерная, упорные', 'пакер с заглушкой']
        self.paker_layout_combo.addItems(paker_layout_list)

        self.swab_true_label_type = QLabel("необходимость освоения", self)
        self.swab_true_edit_type = QComboBox(self)
        self.swab_true_edit_type.addItems(['Нужно освоение', 'без освоения'])

        self.depth_gauge_label = QLabel("глубинные манометры", self)
        self.depth_gauge_combo = QComboBox(self)
        self.depth_gauge_combo.addItems(['Нет', 'Да'])
        self.depth_gauge_combo.setProperty("value", "Нет")

        self.pakerLabel = QLabel("глубина пакера", self)
        self.paker_depth = QLineEdit(self)

        self.paker2Label = QLabel("глубина верхнего пакера", self)
        self.paker2_depth = QLineEdit(self)
        self.paker2_depth.setText(f'{int(self.data_well.perforation_roof - 20)}')

        self.diameter_paker_labelType = QLabel("Диаметр пакера", self)
        self.diameter_paker_edit = QLineEdit(self)

        self.kvost_label = QLabel("Длина хвостовики", self)
        self.paker_khost = QLineEdit(self)

        self.need_privyazka_Label = QLabel("Привязка оборудования", self)
        self.need_privyazka_q_combo = QComboBox()
        self.need_privyazka_q_combo.addItems(['Нет', 'Да'])

        plast_work = ['']
        plast_work.extend(self.data_well.plast_work)

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)

        self.skv_true_label_type = QLabel("необходимость кислотной ванны", self)
        self.svk_true_combo = QComboBox(self)
        self.svk_true_combo.addItems(['Нужно СКВ', 'без СКВ'])

        self.svk_true_combo.setCurrentIndex(1)
        self.skv_acid_label_type = QLabel("Вид кислоты для СКВ", self)
        self.skv_acid_edit = QComboBox(self)
        self.skv_acid_edit.addItems(['HCl', 'HF'])
        self.skv_acid_edit.setCurrentIndex(0)
        self.skv_acid_edit.setProperty('value', 'HCl')
        self.skv_volume_label = QLabel("Объем СКВ", self)
        self.skv_volume_edit = QLineEdit(self)
        self.skv_volume_edit.setText('1')
        self.skv_volume_edit.setClearButtonEnabled(True)
        self.skv_proc_label = QLabel("Концентрация СКВ", self)
        self.skv_proc_edit = QLineEdit(self)
        self.skv_proc_edit.setClearButtonEnabled(True)
        self.skv_proc_edit.setText('15')

        self.sko_true_label_type = QLabel("необходимость СКО", self)
        self.sko_true_combo = QComboBox(self)
        self.sko_true_combo.addItems(['Да', 'Нет'])

        self.Qplast_labelType = QLabel("Нужно ли определять приемистоть до СКО", self)
        self.QplastEdit = QComboBox(self)
        self.QplastEdit.addItems(['ДА', 'НЕТ'])
        self.QplastEdit.setCurrentIndex(1)
        self.QplastEdit.setProperty('value', 'НЕТ')

        self.acid_label_type = QLabel("Вид кислотной обработки", self)
        self.acid_edit = QComboBox(self)
        self.acid_edit.addItems(['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка'])
        self.acid_edit.setCurrentIndex(0)

        self.acid_volume_label = QLabel("Объем кислотной обработки", self)
        self.acid_volume_edit = QLineEdit(self)

        self.acid_volume_edit.setText("10")
        self.acid_volume_edit.setClearButtonEnabled(True)

        self.acid_proc_label = QLabel("Концентрация кислоты", self)
        self.acid_proc_edit = QLineEdit(self)
        self.acid_proc_edit.setText('15')
        self.acid_proc_edit.setClearButtonEnabled(True)

        self.acid_oil_proc_label = QLabel("объем нефти", self)
        self.acid_oil_proc_edit = QLineEdit(self)
        self.acid_oil_proc_edit.setText('0')

        self.swab_type_label = QLabel("задача при освоении", self)
        self.swab_type_combo = QComboBox(self)
        self.swab_type_combo.addItems(['Задача №2.1.13', 'Задача №2.1.14', 'Задача №2.1.16', 'Задача №2.1.11',
                                       'Задача №2.1.16 + герметичность пакера', 'ГРР', 'своя задача'])
        self.swab_type_combo.setCurrentIndex(data_list.swab_type_comboIndex)

        self.swab_pakerLabel = QLabel("Глубина посадки нижнего пакера при освоении", self)
        self.swab_paker_depth = QLineEdit(self)

        self.swab_volumeLabel = QLabel("объем освоения", self)
        self.swab_volume_edit = QLineEdit(self)

        self.iron_label_type = QLabel("необходимость стабилизатора железа", self)
        self.iron_true_combo = QComboBox(self)
        self.iron_true_combo.addItems(['Нет', 'Да'])

        if self.data_well.stabilizator_need:
            self.iron_true_combo.setCurrentIndex(1)

        self.iron_volume_label = QLabel("Объем стабилизатора", self)
        self.iron_volume_edit = QLineEdit(self)
        self.expected_pressure_label = QLabel('Ожидаемое давление закачки')
        self.expected_pressure_edit = QLineEdit(self)
        self.expected_pickup_label = QLabel('Ожидаемая приемистость')
        self.expected_pressure_edit.setValidator(self.validator_int)
        self.expected_pickup_edit = QLineEdit(self)
        self.expected_pickup_edit.setValidator(self.validator_int)
        self.expected_pressure_edit.textChanged.connect(self.update_pressure)
        self.pressure_three_label = QLabel('Режимы ')
        self.pressure_three_edit = QLineEdit(self)

        self.pressure_Label = QLabel("Давление закачки", self)
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setClearButtonEnabled(True)
        self.pressure_edit.setText(str(self.data_well.max_admissible_pressure.get_value))
        self.paker_layout_combo.currentTextChanged.connect(self.update_paker_layout)

        self.Qplast_after_labelType = QLabel("Нужно ли определять приемистоть после СКО", self)
        self.Qplast_after_edit = QComboBox(self)
        self.Qplast_after_edit.addItems(['ДА', 'НЕТ'])

        self.calculate_sko_label = QLabel('Расчет на п.м.')
        self.calculate_sko_line = QLineEdit(self)

        self.paker_depth_zumpf_label = QLabel("Глубина посадки для ЗУМПФа", self)
        self.paker_depth_zumpf_edit = QLineEdit(self)
        self.paker_depth_zumpf_edit.setValidator(self.validator_int)

        self.pressure_zumpf_question_label = QLabel("Нужно ли опрессовывать ЗУМПФ", self)
        self.pressure_zumpf_question_combo = QComboBox(self)
        self.pressure_zumpf_question_combo.addItems(["Нет", "Да"])

        self.grid.addWidget(self.paker_layout_label, 0, 0, 1, 0)
        self.grid.addWidget(self.paker_layout_combo, 1, 0, 1, 0)

        self.grid.addWidget(self.swab_true_label_type, 2, 0)
        self.grid.addWidget(self.swab_true_edit_type, 3, 0)

        self.grid.addWidget(self.plast_label, 2, 1)
        self.grid.addWidget(self.plast_combo, 3, 1)
        self.grid.addWidget(self.depth_gauge_label, 2, 2)
        self.grid.addWidget(self.depth_gauge_combo, 3, 2)
        self.grid.addWidget(self.diameter_paker_labelType, 2, 3)
        self.grid.addWidget(self.diameter_paker_edit, 3, 3)
        self.grid.addWidget(self.kvost_label, 2, 4)
        self.grid.addWidget(self.paker_khost, 3, 4)
        self.grid.addWidget(self.pakerLabel, 2, 5)
        self.grid.addWidget(self.paker_depth, 3, 5)
        self.grid.addWidget(self.paker2Label, 2, 6)
        self.grid.addWidget(self.paker2_depth, 3, 6)
        self.grid.addWidget(self.need_privyazka_Label, 2, 7)
        self.grid.addWidget(self.need_privyazka_q_combo, 3, 7)

        self.grid.addWidget(self.pressure_zumpf_question_label, 2, 8)
        self.grid.addWidget(self.pressure_zumpf_question_combo, 3, 8)
        self.grid.addWidget(self.paker_depth_zumpf_label, 2, 9)
        self.grid.addWidget(self.paker_depth_zumpf_edit, 3, 9)

        self.grid.addWidget(self.skv_true_label_type, 4, 0)
        self.grid.addWidget(self.svk_true_combo, 5, 0)
        self.grid.addWidget(self.skv_acid_label_type, 4, 1)
        self.grid.addWidget(self.skv_acid_edit, 5, 1)
        self.grid.addWidget(self.skv_volume_label, 4, 2)
        self.grid.addWidget(self.skv_volume_edit, 5, 2)
        self.grid.addWidget(self.skv_proc_label, 4, 3)
        self.grid.addWidget(self.skv_proc_edit, 5, 3)
        self.grid.addWidget(self.iron_label_type, 4, 4)
        self.grid.addWidget(self.iron_true_combo, 5, 4)
        self.grid.addWidget(self.iron_volume_label, 4, 5)
        self.grid.addWidget(self.iron_volume_edit, 5, 5)

        self.grid.addWidget(self.sko_true_label_type, 6, 0)
        self.grid.addWidget(self.sko_true_combo, 7, 0)

        self.grid.addWidget(self.acid_label_type, 6, 2)
        self.grid.addWidget(self.acid_edit, 7, 2)
        self.grid.addWidget(self.acid_volume_label, 6, 3)
        self.grid.addWidget(self.acid_volume_edit, 7, 3)
        self.grid.addWidget(self.acid_proc_label, 6, 4)
        self.grid.addWidget(self.acid_proc_edit, 7, 4)
        self.grid.addWidget(self.acid_oil_proc_label, 6, 5)
        self.grid.addWidget(self.acid_oil_proc_edit, 7, 5)
        self.grid.addWidget(self.pressure_Label, 6, 6)
        self.grid.addWidget(self.pressure_edit, 7, 6)
        self.grid.addWidget(self.calculate_sko_label, 6, 8)
        self.grid.addWidget(self.calculate_sko_line, 7, 8)
        self.grid.addWidget(self.Qplast_labelType, 6, 1)
        self.grid.addWidget(self.QplastEdit, 7, 1)
        self.grid.addWidget(self.swab_type_label, 8, 1)
        self.grid.addWidget(self.swab_type_combo, 9, 1)
        self.grid.addWidget(self.swab_pakerLabel, 8, 2)
        self.grid.addWidget(self.swab_paker_depth, 9, 2)
        self.grid.addWidget(self.swab_volumeLabel, 8, 3)
        self.grid.addWidget(self.swab_volume_edit, 9, 3)
        self.grid.addWidget(self.Qplast_after_labelType, 10, 1)
        self.grid.addWidget(self.Qplast_after_edit, 11, 1)

        self.grid.addWidget(self.expected_pickup_label, 10, 2)
        self.grid.addWidget(self.expected_pickup_edit, 11, 2)
        self.grid.addWidget(self.expected_pressure_label, 10, 3)
        self.grid.addWidget(self.expected_pressure_edit, 11, 3)
        self.grid.addWidget(self.pressure_three_label, 10, 4)
        self.grid.addWidget(self.pressure_three_edit, 11, 4)

        self.Qplast_after_edit.currentTextChanged.connect(self.update_q_plast_after)

        if all([self.data_well.dict_perforation[plast]['отрайбировано'] for plast in self.data_well.plast_work]):
            self.paker_layout_combo.setCurrentIndex(2)
        else:
            self.paker_layout_combo.setCurrentIndex(1)

        self.swab_true_edit_type.currentTextChanged.connect(self.update_need_swab)
        self.swab_true_edit_type.setCurrentIndex(1)

        self.paker_depth.textChanged.connect(self.update_paker_depth)
        self.paker_depth.textChanged.connect(self.update_paker_edit)
        self.paker2_depth.textChanged.connect(self.update_paker_edit)

        self.svk_true_combo.currentTextChanged.connect(self.update_skv_edit)
        self.svk_true_combo.setCurrentIndex(0)
        self.svk_true_combo.setCurrentIndex(1)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_paker_edit)
        self.iron_volume_edit.setText(f'{round(float(self.acid_volume_edit.text()), 1) * 10}')
        self.acid_volume_edit.textChanged.connect(self.change_volume_acid)
        self.acid_edit.currentTextChanged.connect(self.update_sko_type)
        self.Qplast_after_edit.setCurrentIndex(1)
        self.Qplast_after_edit.setCurrentIndex(0)

        if self.data_well.curator == 'ОР':
            self.Qplast_after_edit.setCurrentIndex(0)
        else:
            self.Qplast_after_edit.setCurrentIndex(1)
        self.calculate_sko_line.editingFinished.connect(self.update_calculate_sko)

        self.pressure_zumpf_question_combo.currentTextChanged.connect(self.update_paker_need)
        self.pressure_zumpf_question_combo.setCurrentIndex(1)
        self.pressure_zumpf_question_combo.setCurrentIndex(0)

    def update_paker_need(self, index):
        if index == 'Да':
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

    def update_calculate_sko(self):
        plasts = data_list.texts
        metr_pvr = 0
        for plast in self.data_well.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:
                    for interval in self.data_well.dict_perforation[plast]['интервал']:
                        if interval[1] < self.data_well.current_bottom:
                            metr_pvr += abs(interval[0] - interval[1])
        calculate_sko = self.calculate_sko_line.text()
        if calculate_sko != '':
            calculate_sko = calculate_sko.replace(',', '.')
            self.acid_volume_edit.setText(f'{round(metr_pvr * float(calculate_sko), 1)}')

    def update_q_plast_after(self, index):
        if index == 'ДА':
            try:
                self.expected_pickup_edit.setText(f'{self.data_well.expected_pickup}')
                # print(f'ожидаемая приемистисть{self.data_well.expected_pickup}')
            except Exception:
                pass

            try:
                self.expected_pressure_edit.setText(f'{self.data_well.expected_pressure}')
            except Exception:
                pass

            self.expected_pickup_edit.setText(str(self.data_well.expected_pickup))
            self.expected_pressure_edit.setText(str(self.data_well.expected_pressure))

            self.grid.addWidget(self.expected_pickup_label, 10, 2)
            self.grid.addWidget(self.expected_pickup_edit, 11, 2)
            self.grid.addWidget(self.expected_pressure_label, 10, 3)
            self.grid.addWidget(self.expected_pressure_edit, 11, 3)
            self.grid.addWidget(self.pressure_three_label, 10, 4)
            self.grid.addWidget(self.pressure_three_edit, 11, 4)
        else:
            self.expected_pickup_edit.setParent(None)
            self.expected_pressure_label.setParent(None)
            self.expected_pressure_label.setParent(None)
            self.expected_pressure_edit.setParent(None)
            self.pressure_three_label.setParent(None)
            self.pressure_three_edit.setParent(None)

    def update_sko_type(self, type_sko):
        if type_sko == 'ВТ':
            self.sko_vt_label = QLabel('Высокотехнологическое СКО', self)
            self.sko_vt_edit = QLineEdit(self)
            self.grid.addWidget(self.sko_vt_label, 6, 7)
            self.grid.addWidget(self.sko_vt_edit, 7, 7)
        else:
            self.sko_vt_label = QLabel('Высокотехнологическое СКО', self)
            self.sko_vt_edit = QLineEdit(self)
            self.sko_vt_label.setParent(None)
            self.sko_vt_edit.setParent(None)

    def update_pressure(self):
        expected_pressure = self.expected_pressure_edit.text()
        if expected_pressure.isdigit():
            expected_pressure = int(float(expected_pressure))
            self.pressure_three_edit.setText(
                AcidPakerWindow.pressure_mode(self, expected_pressure, self.plast_combo.combo_box.currentText()))

    def change_volume_acid(self):
        if self.acid_volume_edit.text() != '':
            self.iron_volume_edit.setText(f'{round(float(self.acid_volume_edit.text().replace(",", ".")), 1) * 10}')

    def update_paker_depth(self):
        paker_depth = self.paker_depth.text()
        if paker_depth:
            paker_diameter = int(float(self.paker_diameter_select(paker_depth)))
            self.diameter_paker_edit.setText(str(paker_diameter))

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
            self.grid.addWidget(self.paker_depth, 3, 5)
            self.paker2Label.setParent(None)
            self.paker2_depth.setParent(None)

            if index == 'однопакерная, упорный' or 'пакер с заглушкой' == index:
                paker_depth = self.paker_depth.text()
                if paker_depth != '':
                    self.paker_khost.setText(f'{int(self.data_well.current_bottom - int(paker_depth))}')
        elif index in ['двухпакерная', 'двухпакерная, упорные']:
            paker_layout_list_tab = ["Пласт", "хвост", "пакер нижний", 'пакер вверхний', "СКВ",
                                     "вид кислоты", "процент", "объем", "объем нефти"]
            self.grid.addWidget(self.paker2Label, 2, 6)
            self.grid.addWidget(self.paker2_depth, 3, 6)
            self.grid.addWidget(self.pakerLabel, 2, 5)
            self.grid.addWidget(self.paker_depth, 3, 5)
            if index == 'двухпакерная, упорные':
                paker_depth = self.paker_depth.text()
                if paker_depth != '':
                    self.paker_khost.setText(f'{int(self.data_well.current_bottom - int(paker_depth))}')
        elif index in ['воронка']:
            paker_layout_list_tab = ["Пласт", "воронка", "СКВ",
                                     "вид кислоты", "процент", "объем", "объем нефти"]
            self.paker_khost.setText(f'{int(self.data_well.perforation_sole)}')
            self.paker2Label.setParent(None)
            self.paker2_depth.setParent(None)
            self.pakerLabel.setParent(None)
            self.paker_depth.setParent(None)
        elif index in ['ГОНС']:
            paker_layout_list_tab = ["Пласт", "точки", "пом.",
                                     "вид кислоты", "процент", "объем"]
        self.tableWidget.setHorizontalHeaderLabels(paker_layout_list_tab)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

    def update_skv_edit(self, index):
        if index == 'Нужно СКВ':
            self.grid.addWidget(self.skv_acid_label_type, 4, 1)
            self.grid.addWidget(self.skv_acid_edit, 5, 1)
            self.grid.addWidget(self.skv_volume_label, 4, 2)
            self.grid.addWidget(self.skv_volume_edit, 5, 2)
            self.grid.addWidget(self.skv_proc_label, 4, 3)
            self.grid.addWidget(self.skv_proc_edit, 5, 3)
        else:
            self.skv_acid_label_type.setParent(None)
            self.skv_acid_edit.setParent(None)
            self.skv_volume_label.setParent(None)
            self.skv_volume_edit.setParent(None)
            self.skv_proc_label.setParent(None)
            self.skv_proc_edit.setParent(None)

    def update_plast_edit(self):

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
            self.paker_depth.setText(f"{paker_depth}")

            if paker_depth != '':
                self.paker_khost.setText(str(int(sole_plast - paker_depth)))

                self.swab_paker_depth.setText(str(int(roof_plast - 40 - int(float(self.paker_khost.text())))))
        elif self.paker_layout_combo.currentText() in ['однопакерная, упорный', 'пакер с заглушкой']:

            paker_depth = int(roof_plast - 20)
            self.paker_depth.setText(f"{paker_depth}")
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
                self.paker_depth.setText(f"{paker_depth}")
                self.paker2_depth.setText(f"{int(roof_plast - 10)}")
                self.swab_paker_depth.setText(str(paker_depth))
        elif self.paker_layout_combo.currentText() == 'двухпакерная, упорные':
            paker_depth = int(sole_plast + 10)
            if paker_depth != '':
                self.paker_khost.setText(f'{self.data_well.current_bottom - paker_depth}')
                self.paker_depth.setText(f"{paker_depth}")
                self.paker2_depth.setText(f"{int(roof_plast - 10)}")
                self.swab_paker_depth.setText(str(paker_depth))

        # print(f'кровля {roof_plast}, подошва {sole_plast}')

    def update_paker_edit(self):
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
        paker_depth = self.paker_depth.text()

        if self.paker_layout_combo.currentText() in ['однопакерная', 'пакер с заглушкой', 'двухпакерная']:
            if paker_depth != '':
                paker_depth = float(paker_depth)
                for plast in self.data_well.dict_perforation:
                    if any(abs(paker_depth - roof) < 10 or abs(paker_depth - sole) < 10
                           for roof, sole in self.data_well.dict_perforation[plast]['интервал']):
                        self.need_privyazka_q_combo.setCurrentIndex(1)

        if self.paker_layout_combo.currentText() in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:

            if paker_depth != '':

                self.swab_paker_depth.setText(f'{roof_plast - (int(sole_plast) - int(paker_depth))}')
                if self.paker_layout_combo.currentText() in ['однопакерная, упорный', 'пакер с заглушкой']:
                    self.paker_khost.setText(str(int(self.data_well.current_bottom - int(paker_depth))))
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
                if self.paker_depth.text() != '' and self.paker2_depth.text() != '':
                    self.distance_between_packers = abs(int(self.paker_depth.text()) - int(self.paker2_depth.text()))
                    # print(f' расстояние между пакерами {self.distance_between_packers}')
            else:
                if self.paker_depth.text() != '':
                    self.paker2_depth.setText(f'{int(self.paker_depth.text()) - self.distance_between_packers}')
                    self.paker2_depth.setEnabled(False)

        elif self.paker_layout_combo.currentText() in ['воронка']:
            self.paker_khost.setText(f'{sole_plast}')
            self.swab_paker_depth.setText(f'{roof_plast - 30}')

        # print(f'кровля {roof_plast}, подошва {sole_plast}')

    def update_need_swab(self, index):
        if index == 'Нужно освоение':
            self.grid.addWidget(self.swab_type_label, 8, 1)
            self.grid.addWidget(self.swab_type_combo, 9, 1)
            self.grid.addWidget(self.swab_pakerLabel, 8, 2)
            self.grid.addWidget(self.swab_paker_depth, 9, 2)
            self.grid.addWidget(self.swab_volumeLabel, 8, 3)
            self.grid.addWidget(self.swab_volume_edit, 9, 3)
            if self.data_well.region in ['КГМ', 'АГМ']:
                self.swab_type_combo.setCurrentIndex(2)
                self.swab_volume_edit.setText('20')
            else:
                self.swab_type_combo.setCurrentIndex(0)
                self.swab_volume_edit.setText('25')
        else:
            self.swab_type_label.setParent(None)
            self.swab_type_combo.setParent(None)
            self.swab_pakerLabel.setParent(None)
            self.swab_paker_depth.setParent(None)
            self.swab_volumeLabel.setParent(None)
            self.swab_volume_edit.setParent(None)


class TabWidget(TabWidgetUnion):
    def __init__(self, tableWidget, parent=None):
        super().__init__()
        self.addTab(TabPageSoAcid(tableWidget, parent), 'Кислотная обработка')





class AcidPakerWindow(WindowUnion):

    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)

        self.expected_pickup = None
        self.data_well = data_well
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
        self.tabWidget = TabWidget(self.tableWidget, self.data_well)

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
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonadd_string, 2, 0)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)

        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0, 1, 0)

    def add_string(self):

        paker_layout_combo = str(self.tabWidget.currentWidget().paker_layout_combo.currentText())
        plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())

        acid_edit_list = ['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка']
        acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()
        acid_edit_combo = QComboBox(self)
        acid_edit_combo.addItems(acid_edit_list)
        acid_edit_combo.setCurrentIndex(acid_edit_list.index(acid_edit))

        acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
        acid_proc_edit = int(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.'))
        svk_true_combo_str = str(self.tabWidget.currentWidget().svk_true_combo.currentText())
        acid_oil_proc_edit = self.tabWidget.currentWidget().acid_oil_proc_edit.text()

        svk_true_combo = QComboBox(self)
        svk_true_list = ['Нужно СКВ', 'без СКВ']
        svk_true_combo.addItems(svk_true_list)
        svk_true_combo.setCurrentIndex(svk_true_list.index(svk_true_combo_str))

        if not plast_combo or not acid_edit or not acid_volume_edit or not acid_proc_edit:
            QMessageBox.information(self, 'Внимание', 'Заполните данные по объему')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()

        if paker_layout_combo in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
            paker_khost = self.check_if_none(self.tabWidget.currentWidget().paker_khost.text())
            paker_depth = self.check_if_none(self.tabWidget.currentWidget().paker_depth.text())

            if self.data_well.current_bottom < float(paker_khost + paker_depth) or \
                    0 < paker_khost + paker_depth < self.data_well.current_bottom is False:
                QMessageBox.information(self, 'Внимание',
                                        f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                        f'{self.data_well.current_bottom}м')
                return
            if self.check_true_depth_template(paker_depth) is False:
                return
            if self.true_set_paker(paker_depth) is False:
                return
            if self.check_depth_in_skm_interval(paker_depth) is False:
                return

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setCellWidget(rows, 3, svk_true_combo)
            self.tableWidget.setCellWidget(rows, 4, acid_edit_combo)
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(acid_proc_edit)))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(acid_volume_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(acid_oil_proc_edit)))

            self.tableWidget.setSortingEnabled(False)
        elif paker_layout_combo in ['двухпакерная', 'двухпакерная, упорные']:
            paker_khost = self.check_if_none((self.tabWidget.currentWidget().paker_khost.text()))
            paker_depth = int(self.check_if_none(self.tabWidget.currentWidget().paker_depth.text()))
            paker2_depth = int(self.check_if_none(self.tabWidget.currentWidget().paker2_depth.text()))
            if self.check_true_depth_template(paker_depth) is False:
                return
            if self.true_set_paker(paker_depth) is False:
                return
            if self.check_depth_in_skm_interval(paker_depth) is False:
                return
            if self.check_true_depth_template(paker2_depth) is False:
                return
            if self.true_set_paker(paker2_depth) is False:
                return
            if self.check_depth_in_skm_interval(paker2_depth) is False:
                return

            if self.data_well.current_bottom < float(paker_khost + paker2_depth):
                QMessageBox.information(self, 'Внимание',
                                        f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                        f'{self.data_well.current_bottom}м')
                return
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(paker2_depth)))
            self.tableWidget.setCellWidget(rows, 4, svk_true_combo)
            self.tableWidget.setCellWidget(rows, 5, acid_edit_combo)
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(acid_proc_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(acid_volume_edit)))
        elif paker_layout_combo in ['воронка']:
            paker_depth = int(self.check_if_none(self.tabWidget.currentWidget().paker_depth.text()))

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setCellWidget(rows, 2, svk_true_combo)
            self.tableWidget.setCellWidget(rows, 3, acid_edit_combo)
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(acid_proc_edit)))
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(acid_volume_edit)))

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия

    def add_work(self):

        try:
            self.need_privyazka_q_combo = self.tabWidget.currentWidget().need_privyazka_q_combo.currentText()
            if self.need_privyazka_q_combo == 'Да':
                mes = QMessageBox.question(self, 'Привязка', 'Расстояние между пакером и ИП меньше 10м. '
                                                             'Нужна привязка корректно ли?')
                if mes == QMessageBox.StandardButton.No:
                    return

            self.paker_layout_combo = str(self.tabWidget.currentWidget().paker_layout_combo.currentText())
            swab_true_edit_type = self.tabWidget.currentWidget().swab_true_edit_type.currentText()
            diameter_paker = int(float(self.tabWidget.currentWidget().diameter_paker_edit.text()))
            depth_gauge_combo = str(self.tabWidget.currentWidget().depth_gauge_combo.currentText())
            sko_true_combo = str(self.tabWidget.currentWidget().sko_true_combo.currentText())
            skv_acid_edit = str(self.tabWidget.currentWidget().skv_acid_edit.currentText())
            skv_volume_edit = float(self.tabWidget.currentWidget().skv_volume_edit.text().replace(',', '.'))
            skv_proc_edit = int(self.tabWidget.currentWidget().skv_proc_edit.text().replace(',', '.'))
            pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text())
            QplastEdit = str(self.tabWidget.currentWidget().QplastEdit.currentText())
            acid_oil_proc_edit = self.tabWidget.currentWidget().acid_oil_proc_edit.text()

            iron_true_combo = self.tabWidget.currentWidget().iron_true_combo.currentText()
            iron_volume_edit = self.tabWidget.currentWidget().acid_oil_proc_edit.text()
            self.Qplast_after_edit = self.tabWidget.currentWidget().Qplast_after_edit.currentText()
            self.expected_pickup = self.tabWidget.currentWidget().expected_pickup_edit.text()
            self.expected_pressure = self.tabWidget.currentWidget().expected_pressure_edit.text()
            if self.expected_pressure not in [None, 'None', '', '-', 'атм']:
                self.expected_pressure = int(float(self.expected_pressure))
            self.pressure_three = self.tabWidget.currentWidget().pressure_three_edit.text()

            pressure_zumph_combo = self.tabWidget.currentWidget().pressure_zumpf_question_combo.currentText()

            if pressure_zumph_combo == 'Да':
                paker_khost = self.check_if_none(self.tabWidget.currentWidget().paker_khost.text())
                paker_depth_zumpf = self.tabWidget.currentWidget().paker_depth_zumpf_edit.text()

                if paker_depth_zumpf == '':
                    QMessageBox.warning(self, 'Ошибка', f'не введены глубина опрессовки ЗУМПФа')
                    return
                else:
                    paker_depth_zumpf = int(float(paker_depth_zumpf))

                if paker_khost + paker_depth_zumpf >= self.data_well.current_bottom:
                    QMessageBox.warning(self, 'ОШИБКА', 'Длина хвостовика и пакера ниже текущего забоя')
                    return

                if self.check_true_depth_template(paker_depth_zumpf) is False:
                    return
                if self.true_set_paker(paker_depth_zumpf) is False:
                    return
                if self.check_depth_in_skm_interval(paker_depth_zumpf) is False:
                    return

            else:
                paker_depth_zumpf = 0

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка сохранения данных {type(e).__name__}\n\n{str(e)}')
            return

        rows = self.tableWidget.rowCount()

        if rows == 0:
            QMessageBox.warning(self, "ВНИМАНИЕ", 'Нужно добавить интервалы обработки')
            return

        for row in range(rows):
            if self.paker_layout_combo in ['двухпакерная', 'двухпакерная, упорные']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    if paker_khost < 0:
                        QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
                        return
                    data_list.paker_khost = paker_khost
                else:
                    paker_khost = data_list.paker_khost

                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                paker2_depth = int(float(self.tableWidget.item(row, 3).text()))
                svk_true_combo = self.tableWidget.cellWidget(row, 4).currentText()
                acid_edit = self.tableWidget.cellWidget(row, 5).currentText()
                acid_proc_edit = int(float(self.tableWidget.item(row, 6).text()))
                acid_volume_edit = round(float(self.tableWidget.item(row, 7).text()), 1)
                if acid_edit == 'HCl':
                    self.sko_volume_all += acid_volume_edit
                try:
                    acidOilProc = round(float(self.tableWidget.item(row, 8).text()))
                except Exception:
                    acidOilProc = 0

                if row == 0:
                    work_template_list = self.paker_layout_two(swab_true_edit_type, diameter_paker, paker_khost,
                                                               paker_depth, paker2_depth, depth_gauge_combo,
                                                               iron_true_combo, iron_volume_edit)
                else:
                    work_template_list.append(
                        [f'установить пакера на глубине {paker_depth}/{paker2_depth}м',
                         None, f'установить пакера на глубине {paker_depth}/{paker2_depth}м', None, None,
                         None, None, None, None, None,
                         'мастер КРС', 1.2])
            elif self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    data_list.paker_khost = paker_khost
                else:
                    paker_khost = data_list.paker_khost
                paker_depth = int(float(self.tableWidget.item(row, 2).text().replace(',', '.')))
                svk_true_combo = self.tableWidget.cellWidget(row, 3).currentText()
                acid_edit = self.tableWidget.cellWidget(row, 4).currentText().replace(',', '.')
                acid_proc_edit = int(float(self.tableWidget.item(row, 5).text()))
                acid_volume_edit = round(float(self.tableWidget.item(row, 6).text().replace(',', '.')), 1)
                if acid_edit == 'HCl':
                    self.sko_volume_all += acid_volume_edit

                try:
                    acidOilProc = round(float(self.tableWidget.item(row, 7).text()))
                except Exception:
                    acidOilProc = 0

                if row == 0:
                    work_template_list = self.paker_layout_one(swab_true_edit_type, diameter_paker, paker_khost,
                                                               paker_depth, depth_gauge_combo, pressure_zumph_combo,
                                                               paker_depth_zumpf)
                else:
                    work_template_list.append(
                        [f'установить пакер на глубине {paker_depth}, '
                         f'хвост на глубине {paker_depth + paker_khost}м', None,
                         f'установить пакер на глубине {paker_depth}, '
                         f'хвост на глубине {paker_depth + paker_khost}м', None, None,
                         None, None, None, None, None,
                         'мастер КРС', 1.2])
            elif self.paker_layout_combo in ['пакер с заглушкой']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    data_list.paker_khost = paker_khost
                else:
                    paker_khost = data_list.paker_khost
                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                svk_true_combo = self.tableWidget.cellWidget(row, 3).currentText()
                acid_edit = self.tableWidget.cellWidget(row, 4).currentText()
                acid_proc_edit = int(float(self.tableWidget.item(row, 5).text()))
                acid_volume_edit = round(float(self.tableWidget.item(row, 6).text()), 1)
                if acid_edit == 'HCl':
                    self.sko_volume_all += acid_volume_edit

                try:
                    acidOilProc = round(float(self.tableWidget.item(row, 7).text()))
                except Exception:
                    acidOilProc = 0

                work_template_list = self.paker_layout_one_with_zaglushka(swab_true_edit_type, diameter_paker,
                                                                          paker_khost,
                                                                          paker_depth, depth_gauge_combo)
            elif self.paker_layout_combo in ['воронка']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    data_list.paker_khost = paker_khost
                else:
                    paker_khost = data_list.paker_khost

                svk_true_combo = self.tableWidget.cellWidget(row, 2).currentText()
                acid_edit = self.tableWidget.cellWidget(row, 3).currentText()
                acid_volume_edit = round(float(self.tableWidget.item(row, 4).text()), 1)
                acid_proc_edit = int(float(self.tableWidget.item(row, 5).text()))
                if acid_edit == 'HCl':
                    self.sko_volume_all += acid_volume_edit

                try:
                    acidOilProc = round(float(self.tableWidget.item(row, 6).text()))
                except Exception:
                    acidOilProc = 0

                work_template_list = self.voronka_layout(swab_true_edit_type, paker_khost, depth_gauge_combo)

            if svk_true_combo == 'Нужно СКВ':
                work_template_list.extend(self.skv_acid_work(skv_acid_edit, skv_proc_edit, skv_volume_edit))
            if sko_true_combo == 'Да':
                if "двух" in self.paker_layout_combo:
                    if row == 0 and self.data_well.curator != 'ОР' and rows != 1:
                        work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost, acid_edit,
                                                                 acid_volume_edit, acid_proc_edit, pressure_edit,
                                                                 acid_oil_proc_edit, iron_true_combo, iron_volume_edit,
                                                                 paker_depth, paker2_depth)[:-1])
                    else:
                        work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost, acid_edit,
                                                                 acid_volume_edit, acid_proc_edit, pressure_edit,
                                                                 acid_oil_proc_edit, iron_true_combo, iron_volume_edit,
                                                                 paker_depth, paker2_depth))
                elif "одно" in self.paker_layout_combo or "заглуш" in self.paker_layout_combo:
                    if row == 0 and self.data_well.curator != 'ОР' and rows != 1:
                        work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost, acid_edit,
                                                                 acid_volume_edit, acid_proc_edit, pressure_edit,
                                                                 acid_oil_proc_edit, iron_true_combo, iron_volume_edit,
                                                                 paker_depth)[:-1])
                    else:
                        work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost, acid_edit,
                                                                 acid_volume_edit, acid_proc_edit, pressure_edit,
                                                                 acid_oil_proc_edit, iron_true_combo, iron_volume_edit,
                                                                 paker_depth))
                elif "воронка" in self.paker_layout_combo:
                    work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost, acid_edit,
                                                             acid_volume_edit, acid_proc_edit, pressure_edit,
                                                             acid_oil_proc_edit, iron_true_combo, iron_volume_edit))
        if self.sko_volume_all < 13 and acid_edit == 'HCl':
            mes = QMessageBox.question(self, 'Увеличение объема кислоты',
                                       'С целью проведения кислоты Крезолом необходимо согласовать '
                                       'увеличение объема кислотной обработки на 13м3')
            if mes == QMessageBox.StandardButton.No:
                return

        if swab_true_edit_type == "Нужно освоение":
            try:
                swab_type_combo = str(self.tabWidget.currentWidget().swab_type_combo.currentText())
                swab_volume_edit = int(float(self.tabWidget.currentWidget().swab_volume_edit.text()))
                paker_depth_swab = int(float(self.tabWidget.currentWidget().swab_paker_depth.text()))
                for plast in plast_combo.split(','):
                    if plast in self.data_well.plast_work:
                        if abs(paker_khost + paker_depth_swab - self.data_well.dict_perforation[plast]['кровля']) < 20:
                            mes = QMessageBox.question(self, 'Вопрос',
                                                       f'Расстояние между низом компоновки'
                                                       f' {paker_khost + paker_depth_swab} '
                                                       f'и кровлей ПВР меньше 20м '
                                                       f'{self.data_well.dict_perforation[plast]["кровля"]},'
                                                       f' Продолжить?')
                            if mes == QMessageBox.StandardButton.No:
                                return
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка сохранения данных {type(e).__name__}\n\n{str(e)}')
                return

            if self.paker_layout_combo == 'однопакерная' or self.paker_layout_combo == 'пакер с заглушкой':
                if self.true_set_paker(paker_depth_swab) is False:
                    return
                if self.check_depth_in_skm_interval(paker_depth_swab) is False:
                    return
                if self.check_true_depth_template(paker_depth_swab) is False:
                    return

                swab_work_list = SwabWindow.swabbing_with_paker(self, diameter_paker, paker_depth_swab, paker_khost,
                                                                plast_combo, swab_type_combo, swab_volume_edit,
                                                                depth_gauge_combo)
                if self.paker_layout_combo == 'пакер с заглушкой':
                    swab_work_list.pop(6)
                    swab_work_list = swab_work_list[4:]

            elif self.paker_layout_combo == 'двухпакерная':
                paker_depth_swab = int(self.tabWidget.currentWidget().swab_paker_depth.text())
                if self.check_true_depth_template(paker_depth_swab) is False:
                    return
                if self.true_set_paker(paker_depth_swab) is False:
                    return
                if self.check_depth_in_skm_interval(paker_depth_swab) is False:
                    return

                paker_depth2_swab = paker_depth_swab - (paker_depth - paker2_depth)
                if self.check_true_depth_template(paker_depth2_swab) is False:
                    return
                if self.true_set_paker(paker_depth2_swab) is False:
                    return
                if self.check_depth_in_skm_interval(paker_depth2_swab) is False:
                    return

                swab_work_list = SwabWindow.swabbing_with_2paker(self, diameter_paker, paker_depth_swab,
                                                                 paker_depth2_swab,
                                                                 paker_khost, plast_combo, swab_type_combo,
                                                                 swab_volume_edit, depth_gauge_combo,
                                                                 need_change_zgs_combo='Нет', plast_new='',
                                                                 fluid_new='', pressure_new='')
            elif self.paker_layout_combo == 'воронка':
                swab_work_list = SwabWindow.swabbing_with_voronka(self, paker_khost, plast_combo, swab_type_combo,
                                                                  swab_volume_edit, depth_gauge_combo)

            work_template_list.extend(swab_work_list[-10:])

        else:
            work_template_list.append([None, None,
                                       f'Поднять {self.paker_select} на НКТ{self.data_well.nkt_diam} c глубины '
                                       f'{sum(list(self.dict_nkt.values()))}м с '
                                       f'доливом скважины в '
                                       f'объеме {round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 '
                                       f'удельным весом '
                                       f'{self.data_well.fluid_work}',
                                       None, None, None, None, None, None, None,
                                       'мастер КРС',
                                       liftingNKT_norm(self.data_well.current_bottom, 1)])
        if self.data_well.region == 'ТГМ' and self.data_well.curator == 'ОР' and self.data_well.dict_pump_ecn == 0:
            work_template_list.extend(kot_work(self, self.data_well.current_bottom))

        self.calculate_chemistry(acid_edit, acid_volume_edit)

        self.populate_row(self.insert_index, work_template_list, self.table_widget)
        data_list.pause = False
        self.close()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def paker_layout_two(self, swab_true_edit_type, paker_diameter, paker_khost, paker_depth, paker2_depth,
                         depth_gauge_combo, iron_true_combo, iron_volume_edit):
        from work_py.alone_oreration import privyazka_nkt
        from .opressovka import OpressovkaEK, TabPageSo

        difference_paker = paker_depth - paker2_depth

        if 'упорны' in self.paker_layout_combo:
            paker_type = 'ПУ'
        else:
            paker_type = 'ПРО-ЯМО'

        gidroyakor_str = ''
        if depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ +'
        else:
            mtg_str = ''

        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(paker_depth, swab_true_edit_type)

        if (self.data_well.column_additional is False) or \
                (
                        self.data_well.column_additional is True and paker_depth < self.data_well.head_column_additional.get_value):
            self.paker_select = f'заглушку + сбивной с ввертышем + {mtg_str} НКТ{nkt_diam}м {paker_khost}м ' \
                                f'+ пакер {paker_type}-{paker_diameter}мм (либо аналог) ' \
                                f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                                f'{self.data_well.column_wall_thickness.get_value}мм + ' \
                                f' {mtg_str}  щелевой фильтр НКТ{nkt_diam} L-{difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diameter} + {mtg_str} НКТ{nkt_diam}мм 20м + ' \
                                f'реперный патрубок'
            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ{nkt_diam}м {paker_khost}м  + ' \
                               f'пакер {paker_type}-{paker_diameter}мм + щелевой фильтр НКТ {difference_paker}м ' \
                               f' + пакер ПУ - {paker_diameter} + НКТ{nkt_diam}мм 20м + репер'
            self.dict_nkt = {nkt_diam: float(paker_khost) + float(paker_depth)}

        else:
            gidroyakor_str = 'гидроякорь'
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ{nkt_pod}мм {paker_khost}м  + ' \
                                f'пакер {paker_type}-' \
                                f'{paker_diameter}мм (либо аналог) ' \
                                f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                                f'{self.data_well.column_additional_wall_thickness.get_value}мм + ' \
                                f'щелевой фильтр НКТ{nkt_pod} {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diameter} + НКТ{nkt_pod}мм 20м + репер + НКТ{nkt_pod}' \
                                f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                                f'{gidroyakor_str} {mtg_str}'
            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ{nkt_pod}мм {paker_khost}м  + ' \
                               f'пакер {paker_type}-' \
                               f'{paker_diameter}мм + щелевой фильтр НКТ{nkt_pod} {difference_paker}м ' \
                               f'+ пакер ПУ - {paker_diameter} + НКТ{nkt_pod}мм 20м + репер + НКТ{nkt_pod}' \
                               f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                               f'{gidroyakor_str} {mtg_str}'
            self.dict_nkt = {
                nkt_diam: round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 0),
                nkt_pod: int(float(paker_depth) + float(paker_khost) - round(
                    self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 0))}

        paker_list = [
            [self.paker_short, None,
             f'Спустить {self.paker_select} на НКТ{nkt_diam}мм до '
             f'глубины {paker_depth}/{paker2_depth}м'
             f' с замером, шаблонированием шаблоном {nkt_template}мм. '
             f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [f'Посадить пакер на Н- {paker_depth}/{paker2_depth}м', None,
             f'Посадить пакер на глубине {paker_depth}/{paker2_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.3],
            [OpressovkaEK.testing_pressure(self, paker2_depth)[1], None,
             OpressovkaEK.testing_pressure(self, paker2_depth)[0],
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
            if privyazka_nkt(self)[0] not in paker_list:
                paker_list.insert(1, privyazka_nkt(self)[0])
        if depth_gauge_combo == 'Да':
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
                mtg_count = 2
            elif self.paker_layout_combo in ['воронка']:
                mtg_count = 1
            else:
                mtg_count = 3
            paker_list.insert(0, [f'Заявить {mtg_count} глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить {mtg_count} глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])
        return paker_list

    def select_diameter_nkt(self, paker_depth, swab_true_edit_type):
        if self.data_well.column_additional is True and \
                110 > float(self.data_well.column_additional_diameter.get_value) and \
                paker_depth > self.data_well.head_column_additional.get_value > 1000:
            nkt_diam = 73
            nkt_pod = '60'
            template_nkt_diam = '59.6мм, 47.9мм'
        elif self.data_well.column_additional is True and float(
                self.data_well.column_additional_diameter.get_value) > 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            nkt_diam = 73
            nkt_pod = '73мм со снятыми фасками'
            template_nkt_diam = '59.6'
        elif self.data_well.column_additional and self.data_well.head_column_additional.get_value <= 1000 and \
                swab_true_edit_type == 'Нужно освоение':
            nkt_list = ["60", "73"]
            nkt_diam, ok = QInputDialog.getItem(self, 'выбор диаметра НКТ',
                                                'динамический уровень в скважине ниже головы хвостовика,'
                                                'Выберете диаметр НКТ', nkt_list, 0, False)
            nkt_pod = '60мм'
            template_nkt_diam = '59.6мм, 47.9мм'
        elif self.data_well.column_additional and self.data_well.column_additional_diameter.get_value < 110:
            nkt_diam = '73мм'
            nkt_pod = '60мм'
            template_nkt_diam = '59.6мм, 47.9мм'

        elif self.data_well.column_additional is False and self.data_well.column_diameter.get_value < 110:
            nkt_diam = 60
            nkt_pod = '60мм'
            template_nkt_diam = '47.9мм'
        else:
            nkt_diam = 73
            nkt_pod = '73мм'
            template_nkt_diam = '59.6мм'

        return nkt_diam, nkt_pod, template_nkt_diam

    def paker_layout_one(self, swab_true_edit_type, paker_diameter, paker_khost, paker_depth,
                         depth_gauge_combo, pressure_zumph_combo='Нет', paker_depth_zumpf=0):
        from work_py.alone_oreration import privyazka_nkt
        from .opressovka import OpressovkaEK, TabPageSo
        # print(swab_true_edit_type, paker_diameter, paker_khost, paker_depth, depth_gauge_combo)
        if 'упорны' in self.paker_layout_combo:
            paker_type = 'ПУ'
        else:
            paker_type = 'ПРО-ЯМО'
        gidroyakor_str = ''

        if depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''
        if swab_true_edit_type == 'без освоения' and 'Ойл' in data_list.contractor:
            swab_layout = 'Заглушку + щелевой фильтр'
            swab_layout2 = 'сбивной клапан с ввертышем'
        else:
            swab_layout = 'воронку c свабоограничителем'
            swab_layout2 = ''

        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(paker_depth, swab_true_edit_type)

        if (self.data_well.column_additional is False) or \
                (
                        self.data_well.column_additional is True and paker_depth < self.data_well.head_column_additional.get_value):
            self.paker_select = f'{swab_layout} {mtg_str} + НКТ{nkt_diam}мм {paker_khost}м + ' \
                                f'пакер {paker_type}-' \
                                f'{paker_diameter}мм (либо аналог) ' \
                                f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                                f'{self.data_well.column_wall_thickness.get_value}мм + ' \
                                f'НКТ{nkt_diam}мм 10м {swab_layout2}  {mtg_str} + репер'
            self.paker_short = f'{swab_layout} {mtg_str} + НКТ{nkt_diam}мм {paker_khost}м + ' \
                               f'пакер {paker_type}-' \
                               f'{paker_diameter}мм + ' \
                               f'НКТ{nkt_diam}мм 10м {swab_layout2} {mtg_str} + репер'
            self.dict_nkt = {nkt_diam: float(paker_khost) + float(paker_depth)}

        elif self.data_well.column_additional is True and \
                paker_depth > self.data_well.head_column_additional.get_value:
            gidroyakor_str = 'гидроякорь'
            self.paker_select = f'{swab_layout} 2" + НКТ{nkt_pod} {float(paker_khost)}м + пакер {paker_type}-' \
                                f'{paker_diameter}мм (либо аналог) ' \
                                f'для ЭК {float(self.data_well.column_additional_diameter.get_value)}мм х ' \
                                f'{self.data_well.column_additional_wall_thickness.get_value}мм + {swab_layout2} ' \
                                f'НКТ{nkt_pod} 10м + репер + НКТ{nkt_pod}' \
                                f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                                f'{mtg_str}'
            self.paker_short = f'{swab_layout} 2" + НКТ{nkt_pod} {float(paker_khost)}м + пакер {paker_type}-' \
                               f'{paker_diameter}мм  + {swab_layout2} НКТ{nkt_pod} 10м + репер НКТ{nkt_pod} ' \
                               f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                               f'{mtg_str}'
            self.dict_nkt = {
                nkt_diam: round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 0),
                nkt_pod: int(float(paker_depth) + float(paker_khost) - round(
                    self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 0))}
        if pressure_zumph_combo == 'Нет':
            paker_list = [
                [f' СПО {self.paker_short} до глубины {paker_depth}м, воронкой до {paker_depth + paker_khost}м', None,
                 f'Спустить {self.paker_select} + {gidroyakor_str} на НКТ{nkt_diam}мм до глубины '
                 f'{paker_depth}м, воронкой до {paker_depth + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {nkt_template}мм. '
                 f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
                [f'Посадить пакер на глубине {paker_depth}м', None, f'Посадить пакер на глубине {paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.5],
                [OpressovkaEK.testing_pressure(self, paker_depth)[1], None,
                 OpressovkaEK.testing_pressure(self, paker_depth)[0],
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
                [f' СПО {self.paker_short} до глубины {paker_depth}м, воронкой до {paker_depth + paker_khost}м', None,
                 f'Спустить {self.paker_select} + {gidroyakor_str} на НКТ{nkt_diam}мм до глубины '
                 f'{paker_depth}м, воронкой до {paker_depth + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {nkt_template}мм. '
                 f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
                [f'Опрессовать ЗУМПФ в инт {paker_depth_zumpf} - {self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {paker_depth_zumpf} - '
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
                [f'Приподнять и посадить пакер на глубине {paker_depth}м',
                 None, f'Приподнять и посадить пакер на глубине {paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [OpressovkaEK.testing_pressure(self, paker_depth)[1], None,
                 OpressovkaEK.testing_pressure(self, paker_depth)[0],
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
            if privyazka_nkt(self)[0] not in paker_list:
                paker_list.insert(1, privyazka_nkt(self)[0])

        if depth_gauge_combo == 'Да':
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
                mtg_count = 2
            elif self.paker_layout_combo == 'воронка':
                mtg_count = 1
            else:
                mtg_count = 3
            paker_list.insert(0, [f'Заявить {mtg_count} глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить {mtg_count} глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])

        return paker_list

    def paker_layout_one_with_zaglushka(self, swab_true_edit_type, paker_diameter, paker_khost, paker_depth,
                                        depth_gauge_combo):
        from work_py.alone_oreration import privyazka_nkt

        paker_type = 'ПРО-ЯМО'
        gidroyakor_str = ''

        if depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''

        swab_layout = 'Заглушку + сбивной с ввертышем '

        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(paker_depth, swab_true_edit_type)

        if (self.data_well.column_additional is False) or \
                (
                        self.data_well.column_additional is True and paker_depth < self.data_well.head_column_additional.get_value):
            self.paker_select = f'{swab_layout} {mtg_str} + НКТ{nkt_diam}мм {paker_khost}м + ' \
                                f'пакер {paker_type}-' \
                                f'{paker_diameter}мм (либо аналог) ' \
                                f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                                f'{self.data_well.column_wall_thickness.get_value}мм + ' \
                                f'НКТ{nkt_diam}мм 10м  + щелевой фильтр {mtg_str} + репер'
            self.paker_short = f'{swab_layout} {mtg_str} + НКТ{nkt_diam}мм {paker_khost}м + ' \
                               f'пакер {paker_type}-' \
                               f'{paker_diameter}мм + ' \
                               f'НКТ{nkt_diam}мм 10м + щелевой фильтр {mtg_str} + репер'
            self.dict_nkt = {nkt_diam: float(paker_khost) + float(paker_depth)}

        elif self.data_well.column_additional is True and paker_depth > self.data_well.head_column_additional.get_value:
            gidroyakor_str = 'гидроякорь'
            self.paker_select = f'{swab_layout} 2" + НКТ{nkt_pod} {float(paker_khost)}м + пакер {paker_type}-' \
                                f'{paker_diameter}мм (либо аналог) ' \
                                f'для ЭК {float(self.data_well.column_additional_diameter.get_value)}мм х ' \
                                f'{self.data_well.column_additional_wall_thickness.get_value}мм +' \
                                f'НКТ{nkt_pod} 10м + щелевой фильтр + репер + НКТ{nkt_pod}' \
                                f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                                f'{gidroyakor_str} {mtg_str}'
            self.paker_short = f'{swab_layout} 2" + НКТ{nkt_pod} {float(paker_khost)}м + пакер {paker_type}-' \
                               f'{paker_diameter}мм + НКТ{nkt_pod} 10м + щелевой фильтр ' \
                               f'+ репер НКТ{nkt_pod} ' \
                               f'{round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 1)}м ' \
                               f'{gidroyakor_str} {mtg_str}'
            self.dict_nkt = {
                nkt_diam: round(self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 0),
                nkt_pod: int(float(paker_depth) + float(paker_khost) - round(
                    self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 0))}

        paker_list = [
            [f' СПО {self.paker_short} до глубины {paker_depth}м, заглушкой до {paker_depth + paker_khost}м', None,
             f'Спустить {self.paker_select} + {gidroyakor_str} на НКТ{nkt_diam}мм до глубины '
             f'{paker_depth}м, заглушкой до {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {nkt_template}мм. '
             f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
        ]
        for plast in list(self.data_well.dict_perforation.keys()):
            for interval in self.data_well.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - float(self.data_well.depth_fond_paker_before["after"]))) < 10 or abs(
                        float(interval[0] - float(self.data_well.depth_fond_paker_before["after"]))) < 10:
                    if privyazka_nkt(self)[0] not in paker_list:
                        paker_list.insert(1, privyazka_nkt(self)[0])
        if depth_gauge_combo == 'Да':
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
                mtg_count = 2
            elif self.paker_layout_combo == 'воронка':
                mtg_count = 1
            else:
                mtg_count = 3
            paker_list.insert(0, [f'Заявить {mtg_count} глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить {mtg_count} глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])

        return paker_list

    def voronka_layout(self, swab_true_edit_type, paker_khost, depth_gauge_combo):

        swab_layout = 'воронку со свабоограничителем'
        if depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''

        nkt_diam, nkt_pod, nkt_template = self.select_diameter_nkt(paker_khost, swab_true_edit_type)

        if (self.data_well.column_additional is False) or \
                (
                        self.data_well.column_additional is True and paker_khost < self.data_well.head_column_additional.get_value):
            self.paker_select = f'{swab_layout} НКТ{nkt_diam}мм 10м + репер'
            self.paker_short = f'{swab_layout} НКТ{nkt_diam}мм 10м + репер'

            self.dict_nkt = {nkt_diam: float(paker_khost)}

        elif self.data_well.column_additional is True and float(
                self.data_well.column_additional_diameter.get_value) < 110 and \
                paker_khost > self.data_well.head_column_additional.get_value:

            self.paker_select = f'{swab_layout} 2" + НКТ{nkt_pod}' \
                                f'{round(self.data_well.head_column_additional.get_value - paker_khost, 0)}м ' \
                                f' {mtg_str}'
            self.paker_short = f'{swab_layout} 2" + НКТ{nkt_pod}' \
                               f'{round(self.data_well.head_column_additional.get_value - paker_khost, 0)}м ' \
                               f' {mtg_str}'
            self.dict_nkt = {
                nkt_diam: round(self.data_well.head_column_additional.get_value - paker_khost, 0),
                nkt_pod: float(paker_khost) - round(
                    self.data_well.head_column_additional.get_value - self.data_well.current_bottom, 0)}

        paker_list = [
            [f' СПО {self.paker_short} до глубины {paker_khost}м', None,
             f'Спустить {self.paker_select} +  на НКТ{nkt_diam}мм до глубины '
             f'{paker_khost}м'
             f' с замером, шаблонированием шаблоном {nkt_template}мм. ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_khost, 1)],
        ]

        if depth_gauge_combo == 'Да':
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
                mtg_count = 2
            elif self.paker_layout_combo == 'воронка':
                mtg_count = 1
            else:
                mtg_count = 3
            paker_list.insert(0, [f'Заявить {mtg_count} глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить {mtg_count} глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])

        return paker_list

    def skv_acid_work(self, skv_acid_edit, skv_proc_edit, skv_volume_edit):

        skv_list = [
            [f'Определить приемистость при Р-{self.data_well.max_admissible_pressure.get_value}атм', None,
             f'Определить приемистость при Р-{self.data_well.max_admissible_pressure.get_value}атм '
             f'в присутствии представителя заказчика.'
             f'при отсутствии приемистости произвести установку '
             f'СКВ по согласованию с заказчиком',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 1.2],
            [f'СКВ {skv_acid_edit} {skv_proc_edit}%', None,
             f'Произвести установку СКВ {skv_acid_edit} {skv_proc_edit}% концентрации '
             f'в объеме'
             f' {skv_volume_edit}м3 ({round(skv_volume_edit * 1.12 / 24, 1)}т HCL 24%) (по спец. плану, составляет старший мастер)',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 0.5],
            [None, None,
             f'закачать {skv_acid_edit} {skv_proc_edit}% в объеме V={skv_volume_edit}м3; довести кислоту до пласта '
             f'тех.жидкостью в объеме {volume_vn_nkt(self.dict_nkt)}м3 . ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 0.6],
            [f'реагирование 2 часа.', None, f'реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 2],
            [f'Промывка, Q(повторно)', None,
             f'Промыть скважину тех.жидкостью круговой циркуляцией обратной промывкой в 1,5 '
             f'кратном объеме. Определить приемистость пласта в присутствии '
             f'представителя ЦДНГ (составить акт). '
             f'При отсутствии приемистости СКВ повторить. При необходимости увеличить приемистость '
             f'методом дренирования.',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 0.83 + 0.2 + 0.83 + 0.5 + 0.5]
        ]
        self.calculate_chemistry('HCl', skv_volume_edit)
        return skv_list

    def acid_work(self, QplastEdit, plast_combo, paker_khost, acid_edit,
                  acid_volume_edit, acid_proc_edit, pressure_edit, acid_oil_proc_edit,
                  iron_true_combo, iron_volume_edit, paker_depth=1000,
                  paker2_depth=1000):        
        from work_py.alone_oreration import volume_vn_nkt, well_volume
        paker_list = []

        if QplastEdit == 'ДА':
            paker_list.append(
                [f'Насыщение 5м3.  Q пласт {plast_combo} при '
                 f'Р={self.pressure_mode(self.expected_pressure, plast_combo)}атм', None,
                 f'Произвести насыщение скважины до стабилизации давления закачки '
                 f'не менее 5м3. Опробовать  '
                 f'пласт {plast_combo} на приемистость в трех режимах при '
                 f'Р={self.pressure_mode(self.expected_pressure, plast_combo)}атм в присутствии '
                 f'представителя ЦДНГ. '
                 f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                 f'с подтверждением за 2 часа до '
                 f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {self.expected_pickup}м3/сут '
                 f'при давлении {self.expected_pressure}атм '
                 f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.17 + 0.52 + 0.2 + 0.2 + 0.2])

        if iron_true_combo == 'Да':
            iron_str = f' с добавлением стабилизатор железа (Hi-Iron)  из расчета 10кг на 1тн ({iron_volume_edit}кг)'
        else:
            iron_str = ""

        if acid_edit == 'HCl':

            acid_sel = f'Произвести солянокислотную обработку {plast_combo} в объеме {acid_volume_edit}м3 ' \
                       f'({acid_edit} - {acid_proc_edit} %) {iron_str}' \
                       f' в присутствии представителя Заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={self.data_well.max_admissible_pressure.get_value}атм. \n' \
                       f'(для приготовления соляной кислоты в объеме {acid_volume_edit}м3 - {acid_proc_edit}% ' \
                       f'необходимо ' \
                       f'замешать {round(acid_volume_edit * acid_proc_edit / 24 * 1.118, 1)}т HCL 24% и' \
                       f' пресной воды ' \
                       f'{round(float(acid_volume_edit) - float(acid_volume_edit) * float(acid_proc_edit) / 24 * 1.118, 1)}м3) ' \
                       f'Согласовать с Заказчиком проведение кислотной обработки силами ООО Крезол по технологическому' \
                       f' плану работ СК КРЕЗОЛ. '
            acid_sel_short = f'Произвести  СКО {plast_combo}  в V  {acid_volume_edit}м3  ({acid_edit} -' \
                             f' {acid_proc_edit} %) '
        elif acid_edit == 'ВТ':

            vt = self.tabWidget.currentWidget().sko_vt_edit.text()
            acid_sel = f'Произвести кислотную обработку {plast_combo} {vt} в присутствии представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более' \
                       f' Р={self.data_well.max_admissible_pressure.get_value}атм.'
            acid_sel_short = vt
        elif acid_edit == 'HF':

            acid_sel = f'Произвести кислотную обработку пласта {plast_combo} в объеме  {acid_volume_edit}м3 ' \
                       f'(концентрация в смеси HF 3% / HCl 13%){iron_str} силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления ' \
                       f'закачки не более Р={pressure_edit}атм.'
            acid_sel_short = f'Произвести ГКО пласта {plast_combo}  в V- {acid_volume_edit}м3  ' \
                             f'не более Р={pressure_edit}атм.'
        elif acid_edit == 'Нефтекислотка':
            acid_sel = f'Произвести нефтекислотную обработку пласта {plast_combo} в V=2тн товарной нефти +' \
                       f' {acid_volume_edit}м3  (HCl - {acid_proc_edit} %) + {float(acid_oil_proc_edit) - 2}т товарной ' \
                       f'нефти  {iron_str} силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={self.data_well.max_admissible_pressure.get_value}атм.'
            acid_sel_short = f'нефтекислотную обработку пласта {plast_combo} в V=2тн товарной нефти +' \
                             f' {acid_volume_edit}м3  (HCl - {acid_proc_edit} %) + {float(acid_oil_proc_edit) - 2}т ' \
                             f'товарной нефти '
        elif acid_edit == 'Противогипсовая обработка':
            acid_sel = f'Произвести противогипсовую обработку пласта{plast_combo} в объеме {acid_volume_edit}м3 - ' \
                       f'{20}% раствором каустической соды' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={self.data_well.max_admissible_pressure.get_value}атм.\n'
            acid_sel_short = f'Произвести противогипсовую обработку пласта{plast_combo} в объеме ' \
                             f'{acid_volume_edit}м3 - {20}% не ' \
                             f'более Р={self.data_well.max_admissible_pressure.get_value}атм.\n'
            # print(f'Ожидаемое показатели {self.data_well.expected_pick_up.values()}')
        if self.paker_layout_combo in ['воронка', 'пакер с заглушкой']:
            layout_select = 'Закрыть затрубное пространство'
        elif 'одно' in self.paker_layout_combo:
            layout_select = f'посадить пакер на глубине {paker_depth}м'
        elif 'дву' in self.paker_layout_combo:
            layout_select = f'посадить пакера на глубине {paker_depth}/{paker2_depth}м'

        acid_list_1 = [
            [acid_sel_short, None,
             f'{acid_sel}'
             f'ОБЕСПЕЧИТЬ НАЛИЧИЕ У СОСТАВА ВАХТЫ СИЗ ПРИ КИСЛОТНОЙ ОБРАБОТКИ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', None],
            [None, None,
             f"Закачать кислоту в объеме V={round(volume_vn_nkt(self.dict_nkt), 1)}м3 (внутренний "
             f"объем НКТ)" if acid_volume_edit > volume_vn_nkt(self.dict_nkt)
             else f"Закачать кислоту в "
                  f"объеме {round(acid_volume_edit, 1)}м3, "
                  f"довести кислоту тех жидкостью в объеме "
                  f"{round(volume_vn_nkt(self.dict_nkt) - acid_volume_edit, 1)}м3 ",
             None, None, None, None, None, None, None,
             'мастер КРС', 1.25],
            [None, None,
             layout_select,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.3],
            [None, None,
             ''.join(
                 [f'продавить кислоту тех жидкостью в объеме {round(volume_vn_nkt(self.dict_nkt) + 0.5, 1)}м3 '
                  f'при давлении не '
                  f'более {self.data_well.max_admissible_pressure.get_value}атм. Увеличение давления согласовать'
                  f' с заказчиком' if acid_volume_edit < volume_vn_nkt(
                     self.dict_nkt) else f'продавить кислоту оставшейся кислотой в объеме '
                                         f'{round(acid_volume_edit - volume_vn_nkt(self.dict_nkt), 1)}м3 и тех '
                                         f'жидкостью '
                                         f'в объеме {round(volume_vn_nkt(self.dict_nkt) + 0.5, 1)}м3 '
                                         f'при давлении '
                                         f'не более {self.data_well.max_admissible_pressure.get_value}атм. '
                                         f'Увеличение давления согласовать с заказчиком\n'
                                         f'(в случае поглощения произвести продавку в '
                                         f'V-{round(volume_vn_nkt(self.dict_nkt) * 1.5, 1)}м3 '
                                         f'(1.5-ом объеме НКТ)) ']),
             None, None, None, None, None, None, None,
             'мастер КРС', 6],
            [f'без реагирования' if (
                    self.data_well.region == 'ТГМ' and acid_edit == 'HF') else 'реагирование 2 часа.', None,
             f'без реагирования' if (
                     self.data_well.region == 'ТГМ' and acid_edit == 'HF') else 'реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'мастер КРС', '' if (self.data_well.region == 'ТГМ' and acid_edit == 'HF') else 2],
            [f'Срыв 30мин', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [self.flushing_downhole(paker_depth, paker_khost, self.paker_layout_combo)[1], None,
             self.flushing_downhole(paker_depth, paker_khost, self.paker_layout_combo)[0],
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(well_volume(self, self.data_well.current_bottom))]
        ]

        for row in acid_list_1:
            paker_list.append(row)

        if self.Qplast_after_edit == 'ДА':
            paker_list.append([f'{layout_select}. насыщение 5м3', None,
                               f'{layout_select}. Произвести насыщение скважины до стабилизации '
                               f'давления закачки не менее 5м3. Опробовать  '
                               f'пласт {plast_combo} на приемистость в трех режимах при Р='
                               f'{self.pressure_three}атм в присутствии '
                               f'представителя ЦДНГ. '
                               f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
                               f'подтверждением за 2 часа до '
                               f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {self.expected_pickup}м3/сут при '
                               f'давлении {self.expected_pressure}атм '
                               f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                               None, None, None, None, None, None, None,
                               'мастер КРС', 0.5 + 0.17 + 0.15 + 0.52 + 0.2 + 0.2 + 0.2])

        return paker_list

        # Определение трех режимов давлений при определении приемистости

    # @staticmethod
    def pressure_mode(self, mode, plast):
        mode = int(mode / 10) * 10
        if ('d2ps' in plast.lower() or 'дпаш' in plast.lower()) and self.data_well.region == 'ИГМ':
            mode_str = f'{120}, {140}, {160}'
        elif mode > self.data_well.max_admissible_pressure.get_value:
            mode_str = f'{mode}, {mode - 10}, {mode - 20}'
        else:
            mode_str = f'{mode - 10}, {mode}, {mode + 10}'
        return mode_str

        # промывка скважины после кислотной обработки в зависимости от интервала перфорации и компоновки и текущего
        # забоя

    def flushing_downhole(self, paker_depth, paker_khost, paker_layout):

        self.data_well.fluid_work_short = self.data_well.fluid_work[:4]

        if 'одно' in paker_layout:
            if (self.data_well.perforation_roof - 5 + paker_khost >= self.data_well.current_bottom) or \
                    (all([self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                          self.data_well.plast_work])):
                flushing_downhole_list = f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n ' \
                                         f'При отсутствии циркуляции на скважине промывку исключить, ' \
                                         f'увеличить объем продавки кислотного состава в 1,5 кратном объеме НКТ. \n' \
                                         f'При наличии ЦИРКУЛЯЦИИ: Допустить компоновку до глубины ' \
                                         f'{self.data_well.current_bottom}м. ' \
                                         f'Промыть скважину обратной промывкой ' \
                                         f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} п' \
                                         f'ри расходе жидкости не ' \
                                         f'менее 6-8 л/сек в объеме не менее ' \
                                         f'{round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                         f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ. '
                flushing_downhole_short = f'При наличии ЦИРКУЛЯЦИИ: Допустить ' \
                                          f'до Н- {self.data_well.current_bottom}м. ' \
                                          f'Промыть уд.весом ' \
                                          f'{self.data_well.fluid_work[:4]}' \
                                          f'не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 '

            elif self.data_well.perforation_roof - 5 + paker_khost < self.data_well.current_bottom:
                flushing_downhole_list = f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n ' \
                                         f'При отсутствии циркуляции на скважине промывку исключить, ' \
                                         f'увеличить объем продавки кислотного состава в 1,5 кратном объеме НКТ\n' \
                                         f'При наличии ЦИРКУЛЯЦИИ: Допустить пакер до глубины ' \
                                         f'{int(self.data_well.perforation_roof - 5)}м. ' \
                                         f'(на 5м выше кровли интервала перфорации), низ НКТ до глубины' \
                                         f' {self.data_well.perforation_roof - 5 + paker_khost}м) ' \
                                         f'Промыть скважину обратной промывкой по круговой циркуляции ' \
                                         f'жидкостью уд.весом {self.data_well.fluid_work} при расходе жидкости не ' \
                                         f'менее 6-8 л/сек в объеме не менее ' \
                                         f'{round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                         f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ. \n' \
                                         f'в случае ГНО с НВ промывку от забоя делаем с допуском замковой опоры, ' \
                                         f'в случае НН и ЭЦН и наличия пакера в компоновке выполняем отдельное ' \
                                         f'СПО пера для вымыва продуктов реакции'

                flushing_downhole_short = f'При наличии ЦИРКУЛЯЦИИ: Допустить пакер до H- ' \
                                          f'{int(self.data_well.perforation_roof - 5)}м. ' \
                                          f' низ НКТ до H' \
                                          f' {self.data_well.perforation_roof - 5 + paker_khost}м) ' \
                                          f'Промыть уд.весом {self.data_well.fluid_work} не менее ' \
                                          f'{round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                          f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n' \
                                          f'При отсутствии циркуляции на скважине промывку исключить, ' \
                                          f'увеличить объем продавки кислотного состава в 1,5 кратном объеме НКТ'
        elif 'ворон' in paker_layout:
            flushing_downhole_list = f'При наличии ЦИРКУЛЯЦИИ: Допустить компоновку до глубины ' \
                                     f'{self.data_well.current_bottom}м.' \
                                     f' Промыть скважину обратной промывкой ' \
                                     f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} п' \
                                     f'ри расходе жидкости не ' \
                                     f'менее 6-8 л/сек в объеме не менее ' \
                                     f'{round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                     f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.' \
                                     f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n' \
                                     f'При отсутствии циркуляции произвести замещения продуктов реакции тех ' \
                                     f'жидкостью большей плотностью с последующей промывкой'

            flushing_downhole_short = f'При наличии ЦИРКУЛЯЦИИ: Допустить до Н- {self.data_well.current_bottom}м. Промыть уд.весом ' \
                                      f'{self.data_well.fluid_work}' \
                                      f'не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 '
        else:
            flushing_downhole_list = f'При наличии ЦИРКУЛЯЦИИ: При наличии избыточного давления:' \
                                     f'Промыть скважину обратной промывкой ' \
                                     f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} п' \
                                     f'ри расходе жидкости не ' \
                                     f'менее 6-8 л/сек в объеме не менее ' \
                                     f'{round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                     f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.' \
                                     f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n' \
                                     f'При отсутствии циркуляции произвести замещения продуктов реакции тех ' \
                                     f'жидкостью большей плотностью с последующей промывкой'
            flushing_downhole_short = f'При наличии избыточного давления: Промыть уд.весом ' \
                                      f'{self.data_well.fluid_work_short} ' \
                                      f'не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 '

        return flushing_downhole_list, flushing_downhole_short


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()

    window = AcidPakerWindow(1, 1)
    window.show()
    sys.exit(app.exec_())
