from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.Qt import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QInputDialog, QTabWidget, QPushButton, Qt, QCheckBox
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPalette, QFontMetrics, QStandardItem
from PyQt5.QtWidgets import QVBoxLayout, QStyledItemDelegate, qApp, QMessageBox, QCompleter, QTableWidget, QHeaderView, \
    QTableWidgetItem, QMainWindow

from krs import volume_vn_nkt
from main import MyWindow
from open_pz import CreatePZ
from work_py.rationingKRS import descentNKT_norm, well_volume_norm, liftingNKT_norm
from work_py.swabbing import Swab_Window


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

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())

    def updateText(self):
        CreatePZ.texts = []

        for i in range(self.model().rowCount()):

            if self.model().item(i).checkState() == Qt.Checked:
                # print(self.model().item(i).text())

                CreatePZ.texts.append(self.model().item(i).text())
                # print(f' список пласлов{CreatePZ.texts}')
        text = ", ".join(CreatePZ.texts)
        # print(text)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())


        self.lineEdit().setText(elidedText)



    def addItem(self, text, data=None, checked=False):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked if not checked else Qt.Checked, Qt.CheckStateRole)
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



class TabPage_SO_acid(QWidget):
    def __init__(self, tableWidget, parent=None):
        from work_py.opressovka import TabPage_SO
        super().__init__(parent)
        self.le = QLineEdit()
        self.grid = QGridLayout(self)
        self.tableWidget = tableWidget

        self.paker_layout_label = QLabel("Компоновка пакеров", self)
        self.paker_layout_combo = QComboBox(self)
        paker_layout_list = ['воронка','однопакерная', 'двухпакерная',
         'однопакерная, упорный', 'двухпакерная, упорные', 'ГОНС']
        self.paker_layout_combo.addItems(paker_layout_list)

        self.swabTruelabelType = QLabel("необходимость освоения", self)
        self.swabTrueEditType = QComboBox(self)
        self.swabTrueEditType.addItems(['Нужно освоение', 'без освоения'])

        self.depthGaugeLabel = QLabel("глубинные манометры", self)
        self.depth_gauge_combo = QComboBox(self)
        self.depth_gauge_combo.addItems(['Нет', 'Да'])
        self.depth_gauge_combo.setProperty("value", "Нет")

        self.swabTrueEditType.setProperty("value", "без освоения")
        self.swabTrueEditType.setCurrentIndex(int(CreatePZ.swabTrueEditType))

        self.pakerLabel = QLabel("глубина пакера", self)
        self.paker_depth = QLineEdit(self)
        self.paker_depth.setText(f"{int(CreatePZ.perforation_sole - 20)}")
        self.paker_depth.textChanged.connect(self.update_paker_edit)

        self.paker2Label = QLabel("глубина верхнего пакера", self)
        self.paker2_depth = QLineEdit(self)
        self.paker2_depth.setText(f"{int(CreatePZ.perforation_sole - 20)}")
        # self.paker2_depth.textChanged.connect(self.update_paker_edit)

        self.diametr_paker_labelType = QLabel("Диаметр пакера", self)
        self.diametr_paker_edit = QLineEdit(self)
        self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(self, int(self.paker_depth.text()))}')

        self.paker_depth.setClearButtonEnabled(True)

        self.khovstLabel = QLabel("Длина хвостовики", self)
        self.paker_khost = QLineEdit(self)



        self.paker_khost.setClearButtonEnabled(True)

        plast_work = CreatePZ.plast_work

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

        self.acidOilProcLabel = QLabel("объем нефти", self)
        self.acidOilProcEdit = QLineEdit(self)
        self.acidOilProcEdit.setText('0')

        self.pressure_Label = QLabel("Давление закачки", self)
        self.swabTypeLabel = QLabel("задача при освоении", self)
        self.swabTypeCombo = QComboBox(self)
        self.swabTypeCombo.addItems(['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'])
        self.swabTypeCombo.setCurrentIndex(CreatePZ.swabTypeComboIndex)
        self.swabTypeCombo.setProperty('value', 'Задача №2.1.16')

        self.swab_pakerLabel = QLabel("Глубина посадки нижнего пакера при освоении", self)
        self.swab_paker_depth = QLineEdit(self)

        self.swab_volumeLabel = QLabel("объем освоения", self)
        self.swab_volumeEdit = QLineEdit(self)
        self.swab_volumeEdit.setText('20')
        
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setClearButtonEnabled(True)
        self.pressure_edit.setText(str(CreatePZ.max_admissible_pressure._value))
        self.paker_layout_combo.currentTextChanged.connect(self.update_paker_layout)

        self.swabTrueEditType.currentTextChanged.connect(self.update_need_swab)
        self.swabTrueEditType.setCurrentIndex(1)


        self.grid.addWidget(self.paker_layout_label, 0, 0, 1, 0)
        self.grid.addWidget(self.paker_layout_combo, 1, 0, 1, 0)

        self.grid.addWidget(self.swabTruelabelType, 2, 0)
        self.grid.addWidget(self.swabTrueEditType, 3, 0)

        self.grid.addWidget(self.plast_label, 2, 1)
        self.grid.addWidget(self.plast_combo, 3, 1)
        self.grid.addWidget(self.depthGaugeLabel, 2, 2)
        self.grid.addWidget(self.depth_gauge_combo, 3, 2)
        self.grid.addWidget(self.diametr_paker_labelType,2, 3)
        self.grid.addWidget(self.diametr_paker_edit, 3, 3)
        self.grid.addWidget(self.khovstLabel, 2, 4)
        self.grid.addWidget(self.paker_khost, 3, 4)
        self.grid.addWidget(self.pakerLabel, 2, 5)
        self.grid.addWidget(self.paker_depth, 3, 5)
        self.grid.addWidget(self.paker2Label, 2, 6)
        self.grid.addWidget(self.paker2_depth, 3, 6)

        # grid.addWidget(self.privyazkaTrueLabelType, 0, 4)
        # grid.addWidget(self.privyazkaTrueEdit, 1, 4)

        self.grid.addWidget(self.skv_true_label_type, 4, 0)
        self.grid.addWidget(self.svk_true_combo, 5, 0)
        self.grid.addWidget(self.skv_acid_label_type, 4, 1)
        self.grid.addWidget(self.skv_acid_edit, 5, 1)
        self.grid.addWidget(self.skv_volume_label, 4, 2)
        self.grid.addWidget(self.skv_volume_edit, 5, 2)
        self.grid.addWidget(self.skv_proc_label, 4, 3)
        self.grid.addWidget(self.skv_proc_edit, 5, 3)

        self.grid.addWidget(self.acid_label_type, 6, 1)
        self.grid.addWidget(self.acid_edit, 7, 1)
        self.grid.addWidget(self.acid_volume_label, 6, 2)
        self.grid.addWidget(self.acid_volume_edit, 7, 2)
        self.grid.addWidget(self.acid_proc_label, 6, 3)
        self.grid.addWidget(self.acid_proc_edit, 7, 3)
        self.grid.addWidget(self.acidOilProcLabel, 6, 4)
        self.grid.addWidget(self.acidOilProcEdit, 7, 4)
        self.grid.addWidget(self.pressure_Label, 6, 5)
        self.grid.addWidget(self.pressure_edit, 7, 5)
        self.grid.addWidget(self.Qplast_labelType, 6, 0)
        self.grid.addWidget(self.QplastEdit, 7, 0)
        self.grid.addWidget(self.swabTypeLabel, 8, 1)
        self.grid.addWidget(self.swabTypeCombo, 9, 1)
        self.grid.addWidget(self.swab_pakerLabel, 8, 2)
        self.grid.addWidget(self.swab_paker_depth, 9, 2)
        self.grid.addWidget(self.swab_volumeLabel, 8, 3)
        self.grid.addWidget(self.swab_volumeEdit, 9, 3)

        if all([CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]):
            self.paker_layout_combo.setCurrentIndex(2)
        else:
            self.paker_layout_combo.setCurrentIndex(1)

        self.svk_true_combo.currentTextChanged.connect(self.update_skv_edit)
        self.svk_true_combo.setCurrentIndex(1)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

    def update_paker_layout(self, index):
        self.paker_layout_index = index


        if index  in ['однопакерная', 'однопакерная, упорный']:
            paker_layout_list_tab = ["Пласт", "хвост", "пакер", "СКВ", "вид кислоты", "процент", "объем", "объем нефти"]
            self.grid.addWidget(self.pakerLabel, 2, 5)
            self.grid.addWidget(self.paker_depth, 3, 5)
            self.paker2Label.setParent(None)
            self.paker2_depth.setParent(None)
            if index == 'однопакерная, упорный':
                paker_depth = self.paker_depth.text()
                if paker_depth != '':
                    self.paker_khost.setText(f'{int(CreatePZ.current_bottom - int(paker_depth))}')
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
                    self.paker_khost.setText(f'{int(CreatePZ.current_bottom - int(paker_depth))}')
        elif index in ['воронка']:
            paker_layout_list_tab = ["Пласт", "воронка", "СКВ",
                                     "вид кислоты", "процент", "объем", "объем нефти"]
            self.paker_khost.setText(f'{int(CreatePZ.perforation_sole)}')
            self.paker2Label.setParent(None)
            self.paker2_depth.setParent(None)
            self.pakerLabel.setParent(None)
            self.paker_depth.setParent(None)
        elif index in ['ГОНС']:
            paker_layout_list_tab = ["Пласт", "точки", "пом.",
                                     "вид кислоты", "процент", "объем"]

        # for i in range(len(paker_layout_list_tab)):
        #     self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
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

    def update_plast_edit(self, index):

        dict_perforation = CreatePZ.dict_perforation
        plasts = CreatePZ.texts
        # print(f'пласты {plasts, len(CreatePZ.texts), len(plasts), CreatePZ.texts}')
        roof_plast = CreatePZ.current_bottom
        sole_plast = 0
        for plast in CreatePZ.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:

                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']
        # print(roof_plast, sole_plast)

        if self.paker_layout_combo.currentText() == 'однопакерная' :
            paker_depth = int(roof_plast - 20)
            self.paker_depth.setText(f"{paker_depth}")

            if paker_depth != '':
                self.paker_khost.setText(str(int(sole_plast - paker_depth)))
                self.swab_paker_depth.setText(str(int(roof_plast - 30 - (sole_plast - paker_depth))))
        elif self.paker_layout_combo.currentText() == 'однопакерная, упорный':
            self.paker_depth.setText(f"{paker_depth}")
            paker_depth = int(roof_plast - 20)
            if paker_depth != '':
                self.paker_khost.setText(str(int(CreatePZ.current_bottom - paker_depth)))
                self.swab_paker_depth.setText(f'{paker_depth}')
        elif self.paker_layout_combo.currentText() in ['двухпакерная']:
            paker_depth = int(sole_plast+10)
            if paker_depth != '':
                if paker_depth + 10 >=CreatePZ.current_bottom:
                    self.paker_khost.setText(f"{10}")
                else:
                    self.paker_khost.setText(f"{1}")
                self.paker_depth.setText(f"{paker_depth}")
                self.paker2_depth.setText(f"{int(roof_plast - 10)}")
                self.swab_paker_depth.setText(str(paker_depth))
        elif self.paker_layout_combo.currentText() == 'двухпакерная, упорные':
            paker_depth = int(sole_plast + 10)
            if paker_depth != '':
                self.paker_khost.setText(f"{CreatePZ.current_bottom - paker_depth}")
                self.paker_depth.setText(f"{paker_depth}")
                self.paker2_depth.setText(f"{int(roof_plast - 10)}")
                self.swab_paker_depth.setText(str(paker_depth))

        # print(f'кровля {roof_plast}, подошва {sole_plast}')
    def update_paker_edit(self):
        dict_perforation = CreatePZ.dict_perforation

        plasts = CreatePZ.texts
        # print(plasts)
        roof_plast = CreatePZ.current_bottom
        sole_plast = 0
        for plast in CreatePZ.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:

                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']
        paker_depth = self.paker_depth.text()
        if self.paker_layout_combo.currentText() in ['однопакерная', 'однопакерная, упорный']:


            if paker_depth != '':
                self.paker_khost.setText(str(int(sole_plast - int(paker_depth))))
                self.swab_paker_depth.setText(f'{roof_plast - (int(sole_plast) - int(paker_depth))}')
                if self.paker_layout_combo.currentText() == 'однопакерная, упорный':
                    self.paker_khost.setText(str(int(CreatePZ.current_bottom - int(paker_depth))))
                    self.swab_paker_depth.setText(f'{paker_depth}')
        elif self.paker_layout_combo.currentText() in ['двухпакерная', 'двухпакерная, упорные']:
            if paker_depth != '':
                self.paker_khost.setText(f'{10}')
                self.swab_paker_depth.setText(f'{paker_depth}')
                if self.paker_layout_combo.currentText() == 'двухпакерная, упорные':
                    self.paker_khost.setText(str(int(CreatePZ.current_bottom - int(paker_depth))))
        elif self.paker_layout_combo.currentText() in ['воронка']:
            self.paker_khost.setText(f'{sole_plast}')
            self.swab_paker_depth.setText(f'{roof_plast-30}')


        # print(f'кровля {roof_plast}, подошва {sole_plast}')

    def update_need_swab(self, index):
        if index == 'Нужно освоение':
            self.grid.addWidget(self.swabTypeLabel, 8, 1)
            self.grid.addWidget(self.swabTypeCombo, 9, 1)
            self.grid.addWidget(self.swab_pakerLabel, 8, 2)
            self.grid.addWidget(self.swab_paker_depth, 9, 2)
            self.grid.addWidget(self.swab_volumeLabel, 8, 3)
            self.grid.addWidget(self.swab_volumeEdit, 9, 3)
        else:
            self.swabTypeLabel.setParent(None)
            self.swabTypeCombo.setParent(None)
            self.swab_pakerLabel.setParent(None)
            self.swab_paker_depth.setParent(None)
            self.swab_volumeLabel.setParent(None)
            self.swab_volumeEdit.setParent(None)



class TabWidget(QTabWidget):
    def __init__(self, tableWidget):
        super().__init__()
        self.addTab(TabPage_SO_acid(tableWidget), 'Кислотная обработка')


class AcidPakerWindow(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # self.table_widget = table_widget
        # self.ins_ind = ins_ind

        self.paker_select = None
        self.dict_nkt = {}
        self.work_window = None
        self.tableWidget = QTableWidget(0, 8)
        self.tabWidget = TabWidget(self.tableWidget)

        if all([CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]):
            self.tableWidget.setHorizontalHeaderLabels(
                ["Пласт", "хвост", "пакер", "пакер", "СКВ", "вид кислоты", "процент", "объем", "объем нефти"])
        else:

            self.tableWidget.setHorizontalHeaderLabels(
                ["Пласт",  "хвост", "пакер", "СКВ", "вид кислоты", "процент", "объем", "объем нефти"])


        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)
        self.buttonAddString = QPushButton('Добавить обработку')
        self.buttonAddString.clicked.connect(self.addString)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAddString, 2, 0)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)

        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAddWork, 3, 0, 1, 0)


    def addString(self):

        paker_layout_combo = str(self.tabWidget.currentWidget().paker_layout_combo.currentText())
        plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
        acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()
       
        acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
        acid_proc_edit = int(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.'))
        svk_true_combo = str(self.tabWidget.currentWidget().svk_true_combo.currentText())
        acidOilProcEdit = self.tabWidget.currentWidget().acidOilProcEdit.text()

        if not plast_combo or not acid_edit or not acid_volume_edit or not acid_proc_edit:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните данные по объему')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        
        if paker_layout_combo in ['однопакерная', 'однопакерная, упорный']:
            paker_khost = self.if_None((self.tabWidget.currentWidget().paker_khost.text()))
            paker_depth = self.if_None(self.tabWidget.currentWidget().paker_depth.text())

            if CreatePZ.current_bottom < float(paker_khost + paker_depth):
                msg = QMessageBox.information(self, 'Внимание',
                                              f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                              f'{CreatePZ.current_bottom}м')
                return
            self.tableWidget.insertRow(rows)    
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(svk_true_combo))
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(acid_edit))
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(acid_proc_edit)))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(acid_volume_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(acidOilProcEdit)))
    
            self.tableWidget.setSortingEnabled(False)
        elif paker_layout_combo in ['двухпакерная', 'двухпакерная, упорные']:
            paker_khost = self.if_None((self.tabWidget.currentWidget().paker_khost.text()))
            paker_depth = self.if_None(self.tabWidget.currentWidget().paker_depth.text())
            paker2_depth = self.if_None(self.tabWidget.currentWidget().paker2_depth.text())
            if CreatePZ.current_bottom < float(paker_khost + paker_depth):
                msg = QMessageBox.information(self, 'Внимание',
                                              f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                              f'{CreatePZ.current_bottom}м')
                return
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(paker2_depth)))
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(svk_true_combo))
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(acid_edit))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(acid_proc_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(acid_volume_edit)))
        elif paker_layout_combo in ['воронка']:
            paker_khost = self.if_None((self.tabWidget.currentWidget().paker_khost.text()))

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))            
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(svk_true_combo))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(acid_edit))
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(acid_proc_edit)))
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(acid_volume_edit)))
            
            

    def addWork(self):

        self.paker_layout_combo = str(self.tabWidget.currentWidget().paker_layout_combo.currentText())
        swabTrueEditType = self.tabWidget.currentWidget().swabTrueEditType.currentText()
        diametr_paker = int(float(self.tabWidget.currentWidget().diametr_paker_edit.text()))
        depth_gauge_combo = str(self.tabWidget.currentWidget().depth_gauge_combo.currentText())
        svk_true_combo = str(self.tabWidget.currentWidget().svk_true_combo.currentText())
        skv_acid_edit = str(self.tabWidget.currentWidget().skv_acid_edit.currentText())
        skv_volume_edit = float(self.tabWidget.currentWidget().skv_volume_edit.text().replace(',', '.'))
        skv_proc_edit = int(self.tabWidget.currentWidget().skv_proc_edit.text().replace(',', '.'))
        pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text())
        QplastEdit = str(self.tabWidget.currentWidget().QplastEdit.currentText())
        acidOilProcEdit = self.tabWidget.currentWidget().acidOilProcEdit.text()



        rows = self.tableWidget.rowCount()

        if rows == 0:
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'Нужно добавить интервалы обработки')
            return

        for row in range(rows):
            if self.paker_layout_combo in ['двухпакерная', 'двухпакерная, упорные']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    CreatePZ.paker_khost = paker_khost
                else:
                    paker_khost = CreatePZ.paker_khost
                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                paker2_depth = int(float(self.tableWidget.item(row, 3).text()))
                svk_true_combo1 = self.tableWidget.item(row, 4).text()
                acid_edit = self.tableWidget.item(row, 5).text()
                acid_volume_edit = round(float(self.tableWidget.item(row, 6).text()), 1)

                acid_proc_edit = int(float(self.tableWidget.item(row, 7).text()))
                try:
                    acidOilProc = round(float(self.tableWidget.item(row, 8).text()))
                except:
                    acidOilProc = 0
                if row == 0:
                    work_template_list = self.paker_layout_two(swabTrueEditType, diametr_paker, paker_khost,
                                                               paker_depth, paker2_depth, depth_gauge_combo)
                else:
                    work_template_list.append(
                    [None, None, f'установить пакера на глубине {paker_depth}/{paker2_depth}м', None, None,
                     None, None, None, None, None,
                     'мастер КРС', 1.2])
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    CreatePZ.paker_khost = paker_khost
                else:
                    paker_khost = CreatePZ.paker_khost
                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                svk_true_combo1 = self.tableWidget.item(row, 3).text()
                acid_edit = self.tableWidget.item(row, 4).text()
                acid_volume_edit = round(float(self.tableWidget.item(row, 5).text()), 1)

                acid_proc_edit = int(float(self.tableWidget.item(row, 6).text()))
                try:
                    acidOilProc = round(float(self.tableWidget.item(row, 7).text()))
                except:
                    acidOilProc = 0


                if row == 0:
                    work_template_list = self.paker_layout_one(swabTrueEditType, diametr_paker, paker_khost,
                                                               paker_depth, depth_gauge_combo)
                else:
                    work_template_list.append(
                        [None, None, f'установить пакер на глубине {paker_depth}, '
                                     f'хвост на глубине {paker_depth + paker_khost}м', None, None,
                         None, None, None, None, None,
                         'мастер КРС', 1.2])
            if self.paker_layout_combo in ['воронка']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    CreatePZ.paker_khost = paker_khost
                else:
                    paker_khost = CreatePZ.paker_khost

                svk_true_combo1 = self.tableWidget.item(row, 2).text()
                acid_edit = self.tableWidget.item(row, 3).text()
                acid_volume_edit = round(float(self.tableWidget.item(row, 4).text()), 1)

                acid_proc_edit = int(float(self.tableWidget.item(row, 5).text()))
                try:
                    acidOilProc = round(float(self.tableWidget.item(row, 6).text()))
                except:
                    acidOilProc = 0


                work_template_list = self.voronka_layout(swabTrueEditType,  paker_khost, depth_gauge_combo)



            if svk_true_combo == 'Нужно СКВ':
                work_template_list.extend(self.skv_acid_work(skv_acid_edit, skv_proc_edit, skv_volume_edit))
            if "двух" in self.paker_layout_combo:
                if row == 0 and CreatePZ.curator != 'ОР' and rows != 1:
                    work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost,  acid_edit,
                      acid_volume_edit, acid_proc_edit, pressure_edit, acidOilProcEdit, paker_depth, paker2_depth)[:-1])
                else:
                    work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost,  acid_edit,
                      acid_volume_edit, acid_proc_edit, pressure_edit, acidOilProcEdit, paker_depth, paker2_depth))
            elif "одно" in self.paker_layout_combo:
                if row == 0 and CreatePZ.curator != 'ОР' and rows != 1:
                    work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost,  acid_edit,
                      acid_volume_edit, acid_proc_edit, pressure_edit, acidOilProcEdit, paker_depth)[:-1])
                else:
                    work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost, acid_edit,
                      acid_volume_edit, acid_proc_edit, pressure_edit, acidOilProcEdit, paker_depth))
            elif "воронка" in self.paker_layout_combo:
                work_template_list.extend(self.acid_work(QplastEdit, plast_combo, paker_khost, acid_edit,
                                                         acid_volume_edit, acid_proc_edit, pressure_edit,
                                                         acidOilProcEdit))


        if swabTrueEditType == "Нужно освоение":
            swabTypeCombo = str(self.tabWidget.currentWidget().swabTypeCombo.currentText())
            swab_volumeEdit = int(float(self.tabWidget.currentWidget().swab_volumeEdit.text()))
            
            if self.paker_layout_combo == 'однопакерная':
                swab_work_list = Swab_Window.swabbing_with_paker(self, diametr_paker, paker_depth, paker_khost,
                                                                 plast_combo, swabTypeCombo, swab_volumeEdit,
                                                                 depth_gauge_combo)
            elif self.paker_layout_combo == 'двухпакерная':
                swab_work_list = Swab_Window.swabbing_with_2paker(self,diametr_paker, paker_depth, paker2_depth,
                                                                  paker_khost, plast_combo, swabTypeCombo,
                                                                  swab_volumeEdit, depth_gauge_combo)
            elif self.paker_layout_combo == 'воронка':
                swab_work_list = Swab_Window.swabbing_with_voronka(self, paker_depth, plast_combo, swabTypeCombo,
                                                       swab_volumeEdit, depth_gauge_combo)
            

            work_template_list.extend(swab_work_list[-10:])
                
        else:
            work_template_list.append([None, None,
                 f'Поднять {self.paker_select} на НКТ{CreatePZ.nkt_diam} c глубины {sum(list(self.dict_nkt.values()))}м с '
                 f'доливом скважины в '
                 f'объеме {round((CreatePZ.current_bottom) * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС',
                 liftingNKT_norm(CreatePZ.current_bottom, 1)])


        CreatePZ.pause = False
        self.close()
        # print(f'в {work_template_list}')
        return work_template_list

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def paker_layout_two(self, swabTrueEditType, paker_diametr, paker_khost, paker_depth, paker2_depth, depth_gauge_combo):
        from work_py.alone_oreration import privyazkaNKT
        from work_py.opressovka import OpressovkaEK, TabPage_SO

        difference_paker = paker2_depth - paker_depth

        if 'упорны' in self.paker_layout_combo:
            paker_type = 'ПУ'
        else:
            paker_type = 'ПРО-ЯМО'

        gidroyakor_str = ''

        if depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''

        if CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
                paker_depth > CreatePZ.head_column_additional._value:
            nkt_int = 60
            nkt_pod = '60мм'
        elif CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
                paker_depth > CreatePZ.head_column_additional._value:
            nkt_int = 73
            nkt_pod = '73мм со снятыми фасками'

        if (CreatePZ.column_additional is False) or \
                (CreatePZ.column_additional is True and paker_depth < CreatePZ.head_column_additional._value):
            self.paker_select = f'заглушку + сбивной с ввертышем + {mtg_str} НКТ{CreatePZ.nkt_diam}м {paker_khost}м  + ' \
                                f'пакер {paker_type}-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr._value}мм х {CreatePZ.column_wall_thickness._value}мм + ' \
                                f' {mtg_str} + щелевой фильтр НКТ{CreatePZ.nkt_diam} {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr} + {mtg_str} НКТ{CreatePZ.nkt_diam}мм 20м + ' \
                                f'реперный патрубок'
            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ{CreatePZ.nkt_diam}м {paker_khost}м  + ' \
                               f'пакер {paker_type}-{paker_diametr}мм + щелевой фильтр НКТ {difference_paker}м ' \
                                f' + пакер ПУ - {paker_diametr} + НКТ{CreatePZ.nkt_diam}мм 20м + репер'
            self.dict_nkt = {CreatePZ.nkt_diam: float(paker_khost) + float(paker_depth)}

        elif CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
                paker_depth > CreatePZ.head_column_additional._value:
            gidroyakor_str = 'гидроякорь'
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ{nkt_pod}мм {paker_khost}м  + пакер {paker_type}-' \
                                f'{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_additional_diametr._value}мм х ' \
                                f'{CreatePZ.column_additional_wall_thickness._value}мм + ' \
                                f'щелевой фильтр НКТ{nkt_pod} {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ{nkt_pod}мм 20м + репер + НКТ{nkt_pod}' \
                                f'{round(CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 1)}м ' \
                                f'{gidroyakor_str} {mtg_str}'
            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ{nkt_pod}мм {paker_khost}м  + пакер {paker_type}-' \
                                f'{paker_diametr}мм + щелевой фильтр НКТ{nkt_pod} {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ{nkt_pod}мм 20м + репер + НКТ{nkt_pod}' \
                                f'{round(CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 1)}м ' \
                                f'{gidroyakor_str} {mtg_str}'
            self.dict_nkt = { CreatePZ.nkt_diam: round(CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 0),
                nkt_int: int(float(paker_depth) + float(paker_khost) - round(
                    CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 0))}

        paker_list = [
            [self.paker_short, None,
             f'Спустить {self.paker_select} {gidroyakor_str} на НКТ{CreatePZ.nkt_diam}мм до '
             f'глубины {paker_depth}/{paker2_depth}м'
             f' с замером, шаблонированием шаблоном {CreatePZ.nkt_template}мм. '
             f'{("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [f'Посадить пакер на Н- {paker_depth}/{paker2_depth}м'
                , None, f'Посадить пакер на глубине {paker_depth}/{paker2_depth}м'
                ,
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
        for plast in list(CreatePZ.dict_perforation.keys()):
            for interval in CreatePZ.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - float(CreatePZ.depth_fond_paker_do["posle"]))) < 10 or abs(
                        float(interval[0] - float(CreatePZ.depth_fond_paker_do["posle"]))) < 10:
                    if privyazkaNKT(self)[0] not in paker_list:
                        paker_list.insert(1, privyazkaNKT(self)[0])
        if depth_gauge_combo == 'Да':
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный']:
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

    def paker_layout_one(self, swabTrueEditType, paker_diametr, paker_khost, paker_depth, depth_gauge_combo):
        from work_py.alone_oreration import privyazkaNKT
        from work_py.opressovka import OpressovkaEK, TabPage_SO

        if 'упорны' in self.paker_layout_combo:
            paker_type = 'ПУ'
        else:
            paker_type = 'ПРО-ЯМО'
        gidroyakor_str = ''

        if depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''
        if swabTrueEditType == 'без освоения':
            swab_layout = 'Заглушку + щелевой фильтр'
            swab_layout2 = 'сбивной клапан с ввертышем'
        else:
            swab_layout = 'воронку'
            swab_layout2 = ''

        if CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
             paker_depth > CreatePZ.head_column_additional._value:
            nkt_int = 60
            nkt_pod = '60мм'
        elif CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
             paker_depth > CreatePZ.head_column_additional._value:
            nkt_int = 73
            nkt_pod = '73мм со снятыми фасками'

        if (CreatePZ.column_additional is False) or \
                (CreatePZ.column_additional is True and paker_depth < CreatePZ.head_column_additional._value ):
            self.paker_select = f'{swab_layout} {mtg_str} + НКТ{CreatePZ.nkt_diam}мм {paker_khost}м + пакер {paker_type}-' \
                                f'{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr._value}мм х {CreatePZ.column_wall_thickness._value}мм + ' \
                                f'НКТ{CreatePZ.nkt_diam}мм 10м {swab_layout2}  {mtg_str} + репер'
            self.paker_short = f'{swab_layout} {mtg_str} + НКТ{CreatePZ.nkt_diam}мм {paker_khost}м + пакер {paker_type}-' \
                                f'{paker_diametr}мм + ' \
                                f'НКТ{CreatePZ.nkt_diam}мм 10м {swab_layout2} {mtg_str} + репер'
            self.dict_nkt = {CreatePZ.nkt_diam: float(paker_khost) + float(paker_depth)}

        elif CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
                paker_depth > CreatePZ.head_column_additional._value:
            gidroyakor_str = 'гидроякорь'
            self.paker_select = f'{swab_layout} 2" + НКТ{nkt_pod} {float(paker_khost)}м + пакер {paker_type}-' \
                                f'{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {float(CreatePZ.column_additional_diametr._value)}мм х ' \
                                f'{CreatePZ.column_additional_wall_thickness._value}мм + {swab_layout2} ' \
                                f'НКТ{nkt_pod} 10м + репер + НКТ{nkt_pod}' \
                                f'{round(CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 1)}м ' \
                                f'{gidroyakor_str} {mtg_str}'
            self.paker_short  = f'{swab_layout} 2" + НКТ{nkt_pod} {float(paker_khost)}м + пакер {paker_type}-' \
                                f'{paker_diametr}мм  + {swab_layout2} НКТ{nkt_pod} 10м + репер НКТ{nkt_pod} '\
                                f'{round(CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 1)}м ' \
                                f'{gidroyakor_str} {mtg_str}'
            self.dict_nkt = {
                CreatePZ.nkt_diam: round(CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 0),
                 nkt_int: int(float(paker_depth) + float(paker_khost) - round(
                     CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 0))}


        paker_list = [
            [f' СПО {self.paker_short} до глубины {paker_depth}м, воронкой до {paker_depth + paker_khost}м', None,
             f'Спустить {self.paker_select} + {gidroyakor_str} на НКТ{CreatePZ.nkt_diam}мм до глубины '
             f'{paker_depth}м, воронкой до {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {CreatePZ.nkt_template}мм. '
             f'{("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [f'Посадить пакер на глубине {paker_depth}м', None, f'Посадить пакер на глубине {paker_depth}м'
                ,
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
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None]]
        for plast in list(CreatePZ.dict_perforation.keys()):
            for interval in CreatePZ.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - float(CreatePZ.depth_fond_paker_do["posle"]))) < 10 or abs(
                        float(interval[0] - float(CreatePZ.depth_fond_paker_do["posle"]))) < 10:
                    if privyazkaNKT(self)[0] not in paker_list:
                        paker_list.insert(1, privyazkaNKT(self)[0])
        if depth_gauge_combo == 'Да':
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный']:
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

    def voronka_layout(self, swabTrueEditType, paker_khost, depth_gauge_combo):


        swab_layout = 'воронку со свабоограничителем'
        if depth_gauge_combo == 'Да':
            mtg_str = 'контейнер с манометром МТГ'
        else:
            mtg_str = ''


        if CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
                paker_khost > CreatePZ.head_column_additional._value:
            nkt_int = 60
            nkt_pod = '60мм'
        elif CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
                paker_khost > CreatePZ.head_column_additional._value:
            nkt_int = 73
            nkt_pod = '73мм со снятыми фасками'

        if (CreatePZ.column_additional is False) or \
                (CreatePZ.column_additional is True and paker_khost < CreatePZ.head_column_additional._value):
            self.paker_select = f'{swab_layout} НКТ{CreatePZ.nkt_diam}мм 10м + репер'
            self.paker_short = f'{swab_layout} НКТ{CreatePZ.nkt_diam}мм 10м + репер'

            self.dict_nkt = {CreatePZ.nkt_diam: float(paker_khost)}

        elif CreatePZ.column_additional is True and float(CreatePZ.column_additional_diametr._value) < 110 and \
                paker_khost > CreatePZ.head_column_additional._value:

            self.paker_select = f'{swab_layout} 2" + НКТ{nkt_pod}' \
                                f'{round(CreatePZ.head_column_additional.value - paker_khost, 0)}м ' \
                                f' {mtg_str}'
            self.paker_short = f'{swab_layout} 2" + НКТ{nkt_pod}' \
                                f'{round(CreatePZ.head_column_additional.value - paker_khost, 0)}м ' \
                                f' {mtg_str}'
            self.dict_nkt = {
                CreatePZ.nkt_diam: round(CreatePZ.head_column_additional.value - paker_khost, 0),
                nkt_int: float(paker_khost) - round(
                    CreatePZ.head_column_additional.value - CreatePZ.current_bottom, 0)}

        paker_list = [
            [f' СПО {self.paker_short} до глубины {paker_khost}м', None,
             f'Спустить {self.paker_select} +  на НКТ{CreatePZ.nkt_diam}мм до глубины '
             f'{paker_khost}м'
             f' с замером, шаблонированием шаблоном {CreatePZ.nkt_template}мм. ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_khost, 1)],
            ]

        if depth_gauge_combo == 'Да':
            if self.paker_layout_combo in ['однопакерная', 'однопакерная, упорный']:
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
            [f'Определить приемистость при Р-{CreatePZ.max_admissible_pressure._value}атм', None,
             f'Определить приемистость при Р-{CreatePZ.max_admissible_pressure._value}атм '
             f'в присутствии представителя заказчика.'
             f'при отсутствии приемистости произвести установку '
             f'СКВ по согласованию с заказчиком',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 1.2],
            [f'СКВ {skv_acid_edit} {skv_proc_edit}%', None,
             f'Произвести установку СКВ {skv_acid_edit} {skv_proc_edit}% концентрации '
             f'в объеме'
             f' {skv_volume_edit}м3 (0,7т HCL 24%)(по спец. плану, составляет старший мастер)',
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
             f'кратном обьеме. Посадить пакер. Определить приемистость пласта в присутствии '
             f'представителя ЦДНГ (составить акт). Сорвать пакер. '
             f'При отсутствии приемистости СКВ повторить. При необходимости увеличить приемистость '
             f'методом дренирования.',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 0.83 + 0.2 + 0.83 + 0.5 + 0.5]
        ]
        return skv_list
    def acid_work(self, QplastEdit, plast_combo, paker_khost,  acid_edit,
                      acid_volume_edit, acid_proc_edit, pressure_edit, acidOilProcEdit, paker_depth=1000, paker2_depth=1000):
        from krs import volume_vn_nkt
        from krs import well_volume
        paker_list = []

        if QplastEdit == 'ДА' and CreatePZ.curator == 'ОР':
            work_list = []
            work_list.append(
                [f'Насыщение 5м3. Определение Q  пласт {plast_combo} при '
                 f'Р={self.pressure_mode(CreatePZ.expected_P, plast_combo)}атм', None,
                 f'Произвести насыщение скважины до стабилизации давления закачки '
                  f'не менее 5м3. Опробовать  '
                  f'пласт {plast_combo} на приемистость в трех режимах при '
                  f'Р={self.pressure_mode(CreatePZ.expected_P, plast_combo)}атм в присутствии '
                  f'представителя ЦДНГ. '
                  f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                  f'с подтверждением за 2 часа до '
                  f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {CreatePZ.expected_Q}м3/сут '
                  f'при давлении {CreatePZ.expected_P}атм '
                  f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                  None, None, None, None, None, None, None,
                  'мастер КРС', 0.17 + 0.52 + 0.2 + 0.2 + 0.2])
        print(f'rbckjn {acid_edit}')

        if acid_edit == 'HCl':

            acid_sel = f'Произвести  солянокислотную обработку {plast_combo} в объеме {acid_volume_edit}м3 ' \
                       f'({acid_edit} - {acid_proc_edit} %) ' \
                       f' в присутствии представителя Заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={CreatePZ.max_admissible_pressure._value}атм. \n' \
                       f'(для приготовления соляной кислоты в объеме {acid_volume_edit}м3 - {acid_proc_edit}% необходимо ' \
                       f'замешать {round(acid_volume_edit * acid_proc_edit / 24 * 1.118, 1)}т HCL 24% и' \
                       f' пресной воды {round(float(acid_volume_edit) - float(acid_volume_edit) * float(acid_proc_edit) / 24 * 1.118, 1)}м3) ' \
                       f'Согласовать с Заказчиком проведение кислотной обработки силами ООО Крезол. '
            acid_sel_short = f'Произвести  СКО {plast_combo}  в V  {acid_volume_edit}м3  ({acid_edit} - {acid_proc_edit} %) '
        elif acid_edit == 'ВТ':

            vt, ok = QInputDialog.getText(None, 'Высокотехнологическая кислоты', 'Нужно расписать вид кислоты и объем')
            acid_sel = f'Произвести кислотную обработку {plast_combo} {vt}  в присутствии представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более' \
                       f' Р={CreatePZ.max_admissible_pressure._value}атм.'
            acid_sel_short = vt
        elif acid_edit == 'HF':

            acid_sel = f'Произвести кислотную обработку пласта {plast_combo}  в объеме  {acid_volume_edit}м3  ' \
                       f'(концентрация в смеси HF 3% / HCl 13%) силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления ' \
                       f'закачки не более Р={pressure_edit}атм.'
            acid_sel_short = f'Произвести ГКО пласта {plast_combo}  в V- {acid_volume_edit}м3  ' \
                       f'не более Р={pressure_edit}атм.'
        elif acid_edit == 'Нефтекислотка':
            acid_sel = f'Произвести нефтекислотную обработку пласта {plast_combo} в V=2тн товарной нефти +' \
                       f' {acid_volume_edit}м3  (HCl - {acid_proc_edit} %) + {float(acidOilProcEdit) - 2}т товарной нефти ' \
                       f'силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={CreatePZ.max_admissible_pressure._value}атм.'
            acid_sel_short = f'нефтекислотную обработку пласта {plast_combo} в V=2тн товарной нефти +' \
                       f' {acid_volume_edit}м3  (HCl - {acid_proc_edit} %) + {float(acidOilProcEdit) - 2}т товарной нефти'
        elif acid_edit == 'Противогипсовая обработка':
            acid_sel = f'Произвести противогипсовую обработку пласта{plast_combo} в объеме {acid_volume_edit}м3 - {20}% ' \
                       f'раствором каустической соды' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={CreatePZ.max_admissible_pressure._value}атм.\n'
            acid_sel_short = f'Произвести противогипсовую обработку пласта{plast_combo} в объеме {acid_volume_edit}м3 - ' \
                             f'{20}% не ' \
                       f'более Р={CreatePZ.max_admissible_pressure._value}атм.\n'
            # print(f'Ожидаемое показатели {CreatePZ.expected_pick_up.values()}')
        if self.paker_layout_combo == 'воронка':
            layout_select = 'Закрыть затрубное пространство'
        elif 'одно' in self.paker_layout_combo:
            layout_select = f'посадить пакер на глубине {paker_depth}м'
        elif 'дву' in self.paker_layout_combo:
            layout_select = f'посадить пакера на глубине {paker_depth}/{paker2_depth}м'
        acid_list_1 = [[acid_sel_short, None,
                        f'{acid_sel}'
                        f'ОБЕСПЕЧИТЬ НАЛИЧИЕ У СОСТАВА ВАХТЫ СИЗ ПРИ КИСЛОТНОЙ ОБРАБОТКИ',
                        None, None, None, None, None, None, None,
                        'мастер КРС, УСРСиСТ', None],
                       [None, None,
                        f"Закачать кислоту в объеме V={round(volume_vn_nkt(self.dict_nkt), 1)}м3 (внутренний "
                     f"объем НКТ)" if acid_volume_edit > volume_vn_nkt(self.dict_nkt)
                        else f"Закачать кислоту в "
                        f"объеме {round(acid_volume_edit, 1)}м3, "
                        f"довести кислоту тех жидкостью в объеме {round(volume_vn_nkt(self.dict_nkt) - acid_volume_edit, 1)}м3 ",
                        None, None, None, None, None, None, None,
                        'мастер КРС', 1.25],
                       [None, None,
                        layout_select,
                        None, None, None, None, None, None, None,
                        'мастер КРС', 0.3],
                       [None, None,
                        ''.join(
                            [ f'продавить кислоту тех жидкостью в объеме {round(volume_vn_nkt(self.dict_nkt) * 1.5, 1)}м3 '
                                f'при давлении не '
                                f'более {CreatePZ.max_admissible_pressure._value}атм. Увеличение давления согласовать'
                                f' с заказчиком' if acid_volume_edit < volume_vn_nkt(
                                    self.dict_nkt) else f'продавить кислоту оставшейся кислотой в объеме '
                                                   f'{round(acid_volume_edit - volume_vn_nkt(self.dict_nkt), 1)}м3 и тех жидкостью '
                                                   f'в объеме {round(volume_vn_nkt(self.dict_nkt) * 1.5, 1)}м3 при давлении '
                                                   f'не более {CreatePZ.max_admissible_pressure._value}атм. '
                                                   f'Увеличение давления согласовать с заказчиком']),
                        None, None, None, None, None, None, None,
                        'мастер КРС', 6],
                       [f'без реагирования' if (CreatePZ.region == 'ТГМ' and acid_sel == 'HF') else 'реагирование 2 часа.', None,
                        f'без реагирования' if (CreatePZ.region == 'ТГМ' and acid_sel == 'HF') else 'реагирование 2 часа.',
                        None, None, None, None, None, None, None,
                        'мастер КРС', '' if (CreatePZ.region == 'ТГМ' and acid_sel == 'HF') else 2],

                       [f'Срыв 30мин', None,
                        f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                        f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 0.7],
                       [self.flushingDownhole(paker_depth, paker_khost, 1)[0], None,
                        self.flushingDownhole(paker_depth, paker_khost, 1)[0],
                        None, None, None, None, None, None, None,
                        'мастер КРС', well_volume_norm(well_volume(self, CreatePZ.current_bottom))]
                       ]

        for row in acid_list_1:
            paker_list.append(row)

        if CreatePZ.curator == 'ОР':
            try:
                CreatePZ.expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                              f'Ожидаемая приемистость по пласту {plast_combo} ',
                                                              CreatePZ.expected_Q, 0,
                                                              1600)
                CreatePZ.expected_P, ok = QInputDialog.getInt(self, 'Ожидаемое Давление закачки',
                                                              f'Ожидаемое Давление закачки по пласту {plast_combo}',
                                                              CreatePZ.expected_P, 0,
                                                              250)
            except:
                CreatePZ.expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                              f'Ожидаемая приемистость по пласту {plast_combo} ',
                                                              100, 0,
                                                              1600)
                CreatePZ.expected_P, ok = QInputDialog.getInt(self, f'Ожидаемое Давление закачки',
                                                              f'Ожидаемое Давление закачки по пласту {plast_combo}',
                                                              100, 0,
                                                              250)

            paker_list.append([f'Посадить пакер на {paker_depth}м. насыщение 5м3', None,
                               f'Посадить пакер на {paker_depth}м. Произвести насыщение скважины до стабилизации '
                               f'давления закачки не менее 5м3. Опробовать  '
                               f'пласт {plast_combo} на приемистость в трех режимах при Р='
                               f'{self.pressure_mode(CreatePZ.expected_P, plast_combo)}атм в присутствии представителя ЦДНГ. '
                               f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
                               f'подтверждением за 2 часа до '
                               f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {CreatePZ.expected_Q}м3/сут при '
                               f'давлении {CreatePZ.expected_P}атм '
                               f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                               None, None, None, None, None, None, None,
                               'мастер КРС', 0.5 + 0.17 + 0.15 + 0.52 + 0.2 + 0.2 + 0.2])

        return paker_list

        # Определение трех режимов давлений при определении приемистости

    def pressure_mode(self, mode, plast):
        from open_pz import CreatePZ

        mode = int(mode / 10) * 10
        if ('d2ps' in plast.lower() or 'дпаш' in plast.lower()) and CreatePZ.region == 'ИГМ':
            mode_str = f'{120}, {140}, {160}'
        elif mode > CreatePZ.max_admissible_pressure._value:
            mode_str = f'{mode}, {mode - 10}, {mode - 20}'
        else:
            mode_str = f'{mode - 10}, {mode}, {mode + 10}'

        Qpr, _ = QInputDialog.getText(None, 'Режимы определения приемисости', 'Давления при определении приемистости',
                                   text = mode_str)

        return Qpr

        # промывка скважины после кислотной обработки в зависимости от интервала перфорации и комповноки и текущего забоя

    def flushingDownhole(self, paker_depth, paker_khost, paker_layout):
        from open_pz import CreatePZ
        from work_py.opressovka import OpressovkaEK
        from krs import well_volume


        if (CreatePZ.perforation_roof - 5 + paker_khost >= CreatePZ.current_bottom) or \
                (all( [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work])):
            flushingDownhole_list = f'Допустить компоновку до глубины {CreatePZ.current_bottom}м.' \
                                    f' Промыть скважину обратной промывкой ' \
                                    f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} п' \
                                    f'ри расходе жидкости не ' \
                                    f'менее 6-8 л/сек в объеме не менее ' \
                                    f'{round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                    f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
            flushingDownhole_short = f'Допустить до Н- {CreatePZ.current_bottom}м. Промыть уд.весом ' \
                                     f'{CreatePZ.fluid_work_short}' \
                                     f'не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 '

        elif CreatePZ.perforation_roof - 5 + paker_khost < CreatePZ.current_bottom:
            flushingDownhole_list = f'Допустить пакер до глубины {int(CreatePZ.perforation_roof - 5)}м. ' \
                                    f'(на 5м выше кровли интервала перфорации), низ НКТ до глубины' \
                                    f' {CreatePZ.perforation_roof - 5 + paker_khost}м) ' \
                                    f'Промыть скважину обратной промывкой по круговой циркуляции ' \
                                    f'жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
                                    f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                    f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
            flushingDownhole_short = f'Допустить пакер до H- {int(CreatePZ.perforation_roof - 5)}м. ' \
                                    f' низ НКТ до H' \
                                    f' {CreatePZ.perforation_roof - 5 + paker_khost}м) ' \
                                    f'Промыть уд.весом {CreatePZ.fluid_work} не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 '

        return flushingDownhole_list, flushingDownhole_short

    #
    def addRowTable(self):
        pass

        # swabTrueEditType = self.tabWidget.currentWidget().swabTrueEditType.currentText()
        # if swabTrueEditType == 'Нужно освоение':
        #     CreatePZ.swabTrueEditType = 0
        # else:
        #     CreatePZ.swabTrueEditType = 1
        # plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
        # acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()
        # paker_khost = self.if_None((self.tabWidget.currentWidget().paker_khost.text()))
        # paker_depth = self.if_None(self.tabWidget.currentWidget().paker_depth.text())
        # acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
        # acid_proc_edit = int(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.'))
        #
        #
        # swab_paker = self.if_None(self.tabWidget.currentWidget().swab_paker_depth.text().replace(',', '.'))
        # swab_volume = int(self.tabWidget.currentWidget().swab_volumeEdit.text().replace(',', '.'))
        # swabType = str(self.tabWidget.currentWidget().swabTypeCombo.currentText())
        # acidOilProcEdit = self.tabWidget.currentWidget().acidOilProcEdit.text()
        # pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text())
        #
        #
        # QplastEdit = str(self.tabWidget.currentWidget().QplastEdit.currentText())
        # depth_gauge_combo = str(self.tabWidget.currentWidget().depth_gauge_combo.currentText())
        # # privyazka = str(self.tabWidget.currentWidget().privyazka.currentText())
        # print(paker_khost, paker_depth )
        # # if (self.if_None(paker_khost) == 0 or self.if_None(paker_depth) == 0):
        # #     msg = QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
        # #     return
        # if self.countAcid == 0:
        #     CreatePZ.paker_khost = paker_khost
        #     CreatePZ.paker_depth = paker_depth
        #     CreatePZ.depth_gauge_combo = depth_gauge_combo
        #     CreatePZ.swabType = swabType
        #     CreatePZ.swab_volume = swab_volume
        #     CreatePZ.swab_paker = swab_paker
        #     if swabTrueEditType == 'Нужно освоение':
        #         CreatePZ.swabTrueEditType = 0
        #     else:
        #         CreatePZ.swabTrueEditType = 1
        #
        #     print(f'нужно ли освоение {swabTrueEditType}')
        #     work_list = self.acidSelect(swabTrueEditType, CreatePZ.paker_khost, CreatePZ.paker_depth, depth_gauge_combo, QplastEdit, plast_combo)
        #     CreatePZ.depth_gauge_combo = depth_gauge_combo
        #
        #     for row in self.acid_work(swabTrueEditType, acid_proc_edit, CreatePZ.paker_khost, CreatePZ.paker_depth, skv_acid_edit, acid_edit,
        #                               skv_volume_edit,
        #                               QplastEdit, skv_proc_edit, plast_combo, acidOilProcEdit, acid_volume_edit, svk_true_combo,
        #                               self.dict_nkt, pressure_edit):
        #         work_list.append(row)
        #     self.populate_row(CreatePZ.ins_ind, work_list)
        #     CreatePZ.ins_ind += len(work_list)
        #
        #     if swabType == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'
        #         CreatePZ.swabTypeComboIndex = 0
        #     elif swabType == 'Задача №2.1.16':  # , 'Задача №2.1.11', 'своя задача'
        #         CreatePZ.swabTypeComboIndex = 1
        #     elif swabType == 'Задача №2.1.11':  # , 'Задача №2.1.11', 'своя задача'
        #         CreatePZ.swabTypeComboIndex = 2
        # elif self.countAcid == 1:
        #
        #     self.acidSelect(CreatePZ.swabTrueEditType, CreatePZ.paker_khost, CreatePZ.paker_depth, CreatePZ.depth_gauge_combo,
        #                     QplastEdit, plast_combo)
        #     paker_depth = self.if_None(self.tabWidget.currentWidget().paker_depth.text())
        #
        #
        #
        #     work_list = [
        #         [None, None, f'установить пакер на глубине {paker_depth}м', None, None, None, None, None, None, None,
        #          'мастер КРС', 1.2]]
        #     for row in self.acid_work(CreatePZ.swabTrueEditType, acid_proc_edit, CreatePZ.paker_khost, paker_depth, skv_acid_edit,
        #                               acid_edit,
        #                               skv_volume_edit,
        #                               QplastEdit, skv_proc_edit, plast_combo, acidOilProcEdit, acid_volume_edit, svk_true_combo,
        #                               self.dict_nkt, pressure_edit):
        #         work_list.append(row)
        #     self.populate_row(CreatePZ.ins_ind, work_list)
        #     print(f' индекс строк {CreatePZ.ins_ind}')
        #     CreatePZ.ins_ind += len(work_list)
        #     print(f'второй индекс строк {CreatePZ.ins_ind}')
        #     if swabType == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'
        #         CreatePZ.swabTypeComboIndex = 0
        #     elif swabType == 'Задача №2.1.16':  # , 'Задача №2.1.11', 'своя задача'
        #         CreatePZ.swabTypeComboIndex = 1
        #     elif swabType == 'Задача №2.1.11':  # , 'Задача №2.1.11', 'своя задача'
        #         CreatePZ.swabTypeComboIndex = 2
        #
        # elif self.countAcid == 2:
        #     print(f'ye;yj {CreatePZ.swabTrueEditType}')
        #
        #     if CreatePZ.swabTrueEditType == 0:
        #         work_list = []
        #         swabbing_with_paker = self.swabbing_with_paker(CreatePZ.paker_khost, CreatePZ.swab_paker, CreatePZ.swabType, CreatePZ.swab_volume)
        #         for row in swabbing_with_paker:
        #             work_list.append(row)
        #         if CreatePZ.depth_gauge_combo == 'Да':
        #             work_list.append([None, None,
        #                               f'Подать заявку на вывоз глубинных манометров',
        #                               None, None, None, None, None, None, None,
        #                               'мастер КРС', None])
        #     else:
        #         work_list = [[None, None,
        #                       f'Поднять компоновку на НКТ с доливом скважины в '
        #                       f'объеме {round(paker_depth  * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
        #                       None, None, None, None, None, None, None,
        #                       'мастер КРС',
        #                       liftingNKT_norm(paker_depth , 1.2)]]
        #     self.populate_row(CreatePZ.ins_ind, work_list)
        #     # print(f' индекс строк {CreatePZ.ins_ind}')
        #     CreatePZ.ins_ind += len(work_list)
        #     # print(f'третья индекс строк {CreatePZ.ins_ind}')
        #
        # CreatePZ.pause = False
        # self.close()



    def if_None(self, value):

        if isinstance(value, int) or isinstance(value, float):
            return int(value)

        elif str(value).replace('.','').replace(',','').isdigit():
            if str(round(float(value.replace(',','.')), 1))[-1] == 0:
                print(str(round(float(value.replace(',','.')), 1)))
                return int(float(value.replace(',','.')))
            else:
                return float(value.replace(',','.'))
        else:
            return 0




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()


    window = AcidPakerWindow()
    window.show()
    sys.exit(app.exec_())
