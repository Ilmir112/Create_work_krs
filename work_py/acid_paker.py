from datetime import datetime

import datetime as datetime
from PyQt5 import QtWidgets
from PyQt5.Qt import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QInputDialog, QTabWidget, QPushButton, Qt, QCheckBox
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPalette, QFontMetrics, QStandardItem
from PyQt5.QtWidgets import QVBoxLayout, QStyledItemDelegate, qApp, QMessageBox, QCompleter


from main import MyWindow
from open_pz import CreatePZ


from work_py.rationingKRS import descentNKT_norm, well_volume_norm, liftingNKT_norm

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



class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.le = QLineEdit()


        self.swabTruelabelType = QLabel("необходимость освоения", self)
        self.swabTrueEditType = QComboBox(self)
        self.swabTrueEditType.addItems(['Нужно освоение', 'без освоения'])

        self.depthGaugeLabel = QLabel("глубинные манометры", self)
        self.depthGaugeCombo = QComboBox(self)
        self.depthGaugeCombo.addItems(['Нет', 'Да'])
        self.depthGaugeCombo.setProperty("value", "Нет")

        self.swabTrueEditType.setProperty("value", "без освоения")
        self.swabTrueEditType.setCurrentIndex(int(CreatePZ.swabTrueEditType))

        self.pakerLabel = QLabel("глубина пакера", self)
        self.pakerEdit = QLineEdit(self)
        self.pakerEdit.setText(f"{int(CreatePZ.perforation_sole - 20)}")
        self.pakerEdit.textChanged.connect(self.update_paker_edit)

        self.pakerEdit.setClearButtonEnabled(True)

        self.khovstLabel = QLabel("Длина хвостовики", self)
        self.khvostEdit = QLineEdit(self)
        try:
            a = CreatePZ.khvostEdit
        except:
            CreatePZ.khvostEdit = CreatePZ.perforation_sole - int(self.pakerEdit.text())
        self.khvostEdit.setText(str(CreatePZ.khvostEdit))

        self.khvostEdit.setClearButtonEnabled(True)

        plast_work = CreatePZ.plast_work

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

        self.skv_true_label_type = QLabel("необходимость кислотной ванны", self)
        self.svk_true_edit = QComboBox(self)
        self.svk_true_edit.addItems(['Нужно СКВ', 'без СКВ'])
        self.svk_true_edit.setCurrentIndex(1)
        self.svk_true_edit.setProperty('value', 'без СКВ')

        self.skv_acid_label_type = QLabel("Вид кислоты для СКВ", self)
        self.skv_acid_edit = QComboBox(self)
        self.skv_acid_edit.addItems(['HCl', 'HF'])
        self.skv_acid_edit.setCurrentIndex(0)
        self.skv_acid_edit.setProperty('value', 'HCl')

        self.skv_volume_label = QLabel("Объем СКВ", self)
        self.skv_volume_edit = QLineEdit(self)
        self.skv_volume_edit.setText('1')
        self.skv_volume_edit.setClearButtonEnabled(True)

        if self.svk_true_edit.setCurrentIndex(1) == 'без СКВ':
            self.skv_volume_edit.setEnabled(False)
            self.skv_acid_edit.setEnabled(False)
            self.skv_proc_edit.setEnabled(False)

        self.Qplast_labelType = QLabel("Нужно ли определять приемистоть до СКО", self)
        self.QplastEdit = QComboBox(self)
        self.QplastEdit.addItems(['ДА', 'НЕТ'])
        self.QplastEdit.setCurrentIndex(1)
        self.QplastEdit.setProperty('value', 'НЕТ')

        self.skv_proc_label = QLabel("Концентрация СКВ", self)
        self.skv_proc_edit = QLineEdit(self)
        self.skv_proc_edit.setClearButtonEnabled(True)
        self.skv_proc_edit.setText('15')

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
        self.acidOilProcEdit.setClearButtonEnabled(True)

        self.pressure_Label = QLabel("Давление закачки", self)

        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setClearButtonEnabled(True)
        self.pressure_edit.setText(str(CreatePZ.max_admissible_pressure._value))

        self.swabTypeLabel = QLabel("задача при освоении", self)
        self.swabTypeCombo = QComboBox(self)
        self.swabTypeCombo.addItems(['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11',
                                     'своя задача'])
        self.swabTypeCombo.setCurrentIndex(CreatePZ.swabTypeComboIndex)
        self.swabTypeCombo.setProperty('value', 'Задача №2.1.16')

        self.swab_pakerLabel = QLabel("Глубина посадки пакера при освоении", self)
        self.swab_pakerEdit = QLineEdit(self)

        self.swab_volumeLabel = QLabel("объем освоения", self)
        self.swab_volumeEdit = QLineEdit(self)
        self.swab_volumeEdit.setText('20')

        if CreatePZ.countAcid == 1:
            for enable in [self.khovstLabel, self.khvostEdit, self.swabTruelabelType,
                           self.swabTrueEditType, self.swabTypeCombo, self.depthGaugeCombo]:
                enable.setEnabled(False)
        elif CreatePZ.countAcid == 2:
            listEnabel = [self.khovstLabel, self.khvostEdit, self.swabTruelabelType,
                          self.swabTrueEditType, self.plast_combo,
                          self.svk_true_edit, self.QplastEdit, self.skv_proc_edit,
                          self.acid_edit, self.acid_volume_edit,
                          self.acid_proc_edit, self.depthGaugeCombo, self.pakerEdit, self.acidOilProcEdit]
            for enable in listEnabel:
                enable.setEnabled(False)

        grid = QGridLayout(self)

        grid.addWidget(self.swabTruelabelType, 0, 0)
        grid.addWidget(self.swabTrueEditType, 1, 0)
        grid.addWidget(self.khovstLabel, 0, 3)
        grid.addWidget(self.khvostEdit, 1, 3)
        grid.addWidget(self.plast_label, 0, 1)
        grid.addWidget(self.plast_combo, 1, 1)
        grid.addWidget(self.pakerLabel, 0, 2)
        grid.addWidget(self.pakerEdit, 1, 2)
        # grid.addWidget(self.privyazkaTrueLabelType, 0, 4)
        # grid.addWidget(self.privyazkaTrueEdit, 1, 4)

        grid.addWidget(self.skv_true_label_type, 2, 0)
        grid.addWidget(self.svk_true_edit, 3, 0)
        grid.addWidget(self.skv_acid_label_type, 2, 1)
        grid.addWidget(self.skv_acid_edit, 3, 1)
        grid.addWidget(self.skv_volume_label, 2, 2)
        grid.addWidget(self.skv_volume_edit, 3, 2)
        grid.addWidget(self.skv_proc_label, 2, 3)
        grid.addWidget(self.skv_proc_edit, 3, 3)

        grid.addWidget(self.acid_label_type, 4, 1)
        grid.addWidget(self.acid_edit, 5, 1)
        grid.addWidget(self.acid_volume_label, 4, 2)
        grid.addWidget(self.acid_volume_edit, 5, 2)
        grid.addWidget(self.acid_proc_label, 4, 3)
        grid.addWidget(self.acid_proc_edit, 5, 3)
        grid.addWidget(self.acidOilProcLabel, 4, 4)
        grid.addWidget(self.acidOilProcEdit, 5, 4)
        grid.addWidget(self.pressure_Label, 4, 5)
        grid.addWidget(self.pressure_edit, 5, 5)
        grid.addWidget(self.Qplast_labelType, 4, 0)
        grid.addWidget(self.QplastEdit, 5, 0)
        grid.addWidget(self.swabTypeLabel, 6, 1)
        grid.addWidget(self.swabTypeCombo, 7, 1)
        grid.addWidget(self.swab_pakerLabel, 6, 2)
        grid.addWidget(self.swab_pakerEdit, 7, 2)
        grid.addWidget(self.swab_volumeLabel, 6, 3)
        grid.addWidget(self.swab_volumeEdit, 7, 3)
        grid.addWidget(self.depthGaugeLabel, 6, 4)
        grid.addWidget(self.depthGaugeCombo, 7, 4)

    def update_plast_edit(self):
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

            if dict_perforation[plast]['отрайбировано']:
                paker_depth = int(roof_plast - 8)
                self.pakerEdit.setText(f"{paker_depth}")
                self.khvostEdit.setText(str(int(sole_plast - paker_depth)))
                self.swab_pakerEdit.setText(str(int(paker_depth - 30)))
            else:
                paker_depth = int(roof_plast - 20)
                self.pakerEdit.setText(f"{paker_depth}")
                self.khvostEdit.setText(str(int(sole_plast - paker_depth)))
                self.swab_pakerEdit.setText(str(int(paker_depth - 30)))
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

        if CreatePZ.perforation_roof < roof_plast:
            paker_depth = self.pakerEdit.text()
            if paker_depth:
                self.khvostEdit.setText(str(int(sole_plast - int(paker_depth))))
                self.swab_pakerEdit.setText(str(int(paker_depth) - 30))
        else:
            paker_depth = self.pakerEdit.text()
            if paker_depth:
                self.khvostEdit.setText(str(int(sole_plast - int(paker_depth))))
                self.swab_pakerEdit.setText(str(int(paker_depth) - 30))
        # print(f'кровля {roof_plast}, подошва {sole_plast}')

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Кислотная обработка на одном пакере')


class AcidPakerWindow(MyWindow):

    def __init__(self, table_widget, ins_ind, countAcid, parent=None):

        super(MyWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind
        self.countAcid = countAcid
        self.paker_select = None
        self.tabWidget = TabWidget()
        self.dict_nkt = {}

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.addRowTable)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def swabbing_with_paker(self, paker_khost, paker_depth, swab, swab_volume):
        from work_py.opressovka import OpressovkaEK
        from krs import well_volume
        if swab == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
            swab_select = f'Произвести  геофизические исследования по технологической задаче ' \
                          f'№ 2.1.13 Определение профиля и состава притока, дебита, источника ' \
                          f'обводнения и технического состояния эксплуатационной колонны и НКТ ' \
                          f'после свабирования с отбором жидкости не ' \
                          f'менее {swab_volume}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной ' \
                          f'таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
            swab_short = f'Сваб {swab_volume}м3 + Профиль притока.'
        elif swab == 'Задача №2.1.16':
            swab_select = f'Произвести  геофизические исследования по технологической ' \
                          f'задаче № 2.1.16 Определение дебита и ' \
                          f'обводнённости по прослеживанию уровней, ВНР и по регистрации ' \
                          f'забойного давления после освоения ' \
                          f'свабированием  не менее не ' \
                          f'менее {swab_volume}м3. \n' \
                          f'Пробы при свабировании отбирать в ' \
                          f'стандартной таре на {swab_volume - 10}, ' \
                          f'{swab_volume - 5}, {swab_volume}м3,' \
                          f' своевременно подавать телефонограммы ' \
                          f'на завоз тары и вывоз проб'
            swab_short = f'Сваб {swab_volume}м3 + КВУ, ВНР.'
        elif swab == 'Задача №2.1.11':
            swab_select = f'Произвести  геофизические исследования по ' \
                          f'технологической задаче № 2.1.11  свабирование в объеме не ' \
                          f'менее  {swab_volume}м3. \n ' \
                          f'Отобрать пробу на химический анализ воды на ОСТ-39 при ' \
                          f'последнем рейсе сваба (объем не менее 10литров).' \
                          f'Обязательная сдача в этот день в ЦДНГ'
            swab_short = f'Сваб {swab_volume}м3.'

        paker_list = [
            [f'пакер на H- {paker_depth}м, воронку на H- {paker_khost + paker_depth}м'
                , None, f'Посадить пакер на глубине {paker_depth}м, воронку на глубине {paker_khost + paker_depth}м'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [OpressovkaEK.testing_pressure(self, paker_depth)[1], None,
             OpressovkaEK.testing_pressure(self, paker_depth)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'В случае негерметичности э/к согласовать с заказчиком дальнейшие действия',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным '
             f'инженером от 14.10.2021г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально ожидаемое давление '
             f'на устье {CreatePZ.max_expected_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести '
             f'практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'срыв 30мин. Промывка не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            [f'КВУ 15мин', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоениювыполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового '
             f'давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5],
            [None, None,
             f'Поднять компоновку на НКТ{CreatePZ.nkt_diam} c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС',
             liftingNKT_norm(paker_depth, 1.2)]]
        ovtr = 'ОВТР 4ч' if CreatePZ.region == 'ЧГМ' else 'ОВТР 10ч'
        ovtr4 = 4 if CreatePZ.region == 'ЧГМ' else 10
        if swab == 'Задача №2.1.13' and CreatePZ.region not in ['ИГМ']:
            paker_list.insert(3, [ovtr, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        return paker_list

    def acidSelect(self, swabTrueEditType, khvostEdit, pakerEdit, depthGaugeEdit, QplastEdit, plast_combo):
        from work_py.opressovka import OpressovkaEK, TabPage_SO
        from work_py.alone_oreration import privyazkaNKT
        paker_diametr = TabPage_SO.paker_diametr_select(self, pakerEdit)
        swabTrueEditType = True if swabTrueEditType == 'Нужно освоение' else False
        if depthGaugeEdit == 'Да' and CreatePZ.column_additional is False:
            self.paker_select = f'воронку + контейнер с манометром МТГ + НКТ{CreatePZ.nkt_diam}мм {khvostEdit}м + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr._value}мм х {CreatePZ.column_wall_thickness._value}мм + ' \
                                f'НКТ{CreatePZ.nkt_diam} 10м + контейнер манометром МТГ-25 +репер'
            self.paker_short = f'воронку + контейнер с манометром МТГ + НКТ{CreatePZ.nkt_diam}мм {khvostEdit}м + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм + ' \
                                f'НКТ{CreatePZ.nkt_diam}мм 10м + контейнер манометром МТГ-25 +репер'
            self.dict_nkt = {CreatePZ.nkt_diam: float(khvostEdit) + float(pakerEdit)}

        if (CreatePZ.column_additional == False and swabTrueEditType == True) or (CreatePZ.column_additional is True \
                                                                                  and pakerEdit < CreatePZ.head_column_additional._value and swabTrueEditType is True):
            self.paker_select = f'воронку + НКТ{CreatePZ.nkt_diam}мм {khvostEdit}м + пакер ПРО-ЯМО-' \
                                f'{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr._value}мм х {CreatePZ.column_wall_thickness._value}мм + ' \
                                f'НКТ{CreatePZ.nkt_diam}мм 10м + репер'
            self.paker_short = f'воронку + НКТ{CreatePZ.nkt_diam}мм {khvostEdit}м + пакер ПРО-ЯМО-' \
                                f'{paker_diametr}мм + ' \
                                f'НКТ{CreatePZ.nkt_diam}мм 10м + репер'

            self.dict_nkt = {CreatePZ.nkt_diam: float(khvostEdit) + float(pakerEdit)}

        elif CreatePZ.column_additional == True and float(CreatePZ.column_additional_diametr._value) < 110 and \
                pakerEdit > CreatePZ.head_column_additional._value and swabTrueEditType == True:
            self.paker_select = f'воронку + НКТ{60}мм {float(khvostEdit)}м + пакер ПРО-ЯМО-' \
                                f'{OpressovkaEK.paker_diametr_select(float(pakerEdit))}мм (либо аналог) ' \
                                f'для ЭК {float(CreatePZ.column_additional_diametr._value)}мм х ' \
                                f'{CreatePZ.column_additional_wall_thickness._value}мм + НКТ60мм 10м + репер'
            self.paker_short  = f'воронку + НКТ{60}мм {float(khvostEdit)}м + пакер ПРО-ЯМО-' \
                                f'{OpressovkaEK.paker_diametr_select(float(pakerEdit))}мм  + НКТ60мм 10м + репер'
            self.dict_nkt = {CreatePZ.nkt_diam: CreatePZ.head_column_additional._value,
                             60: int(float(pakerEdit) + float(khvostEdit) - float(CreatePZ.head_column_additional._value))}
        elif CreatePZ.column_additional == True and float(
                CreatePZ.column_additional_diametr._value) > 110 and pakerEdit > CreatePZ.head_column_additional._value and swabTrueEditType == True:
            self.paker_select = f'воронку + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {float(khvostEdit)}м + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {float(CreatePZ.column_additional_diametr._value)}мм х ' \
                                f'{CreatePZ.column_additional_wall_thickness._value}мм + НКТ{CreatePZ.nkt_diam}мм со ' \
                                f'снятыми фасками 10м'
            self.paker_short = f'воронку + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {float(khvostEdit)}м + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм  + НКТ{CreatePZ.nkt_diam}мм со ' \
                                f'снятыми фасками 10м'
            self.dict_nkt = {CreatePZ.nkt_diam: float(pakerEdit) + float(khvostEdit)}
        elif (CreatePZ.column_additional == False and swabTrueEditType == False) or (
                CreatePZ.column_additional == True
                and pakerEdit < float(CreatePZ.head_column_additional._value) and swabTrueEditType == False):
            self.paker_select = f'Заглушку + щелевой фильтр + НКТ{CreatePZ.nkt_diam}мм {float(khvostEdit)}м + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr._value}мм х {CreatePZ.column_wall_thickness._value}мм + НКТ 10м + ' \
                                f'сбивной клапан с ввертышем'
            self.paker_short = f'Заглушку + щелевой фильтр + НКТ{CreatePZ.nkt_diam}мм {float(khvostEdit)}м + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм + НКТ 10м + ' \
                                f'сбивной клапан с ввертышем'
            self.dict_nkt = {CreatePZ.nkt_diam: float(pakerEdit) + float(khvostEdit)}
            # print(f' 5 {CreatePZ.column_additional == False, (CreatePZ.column_additional == True and pakerEdit < CreatePZ.head_column_additional._value), swabTrueEditType == False}')
        elif CreatePZ.column_additional == True or (float(CreatePZ.column_additional_diametr._value) < 110 and (
                pakerEdit > CreatePZ.head_column_additional._value) and swabTrueEditType == False):
            self.paker_select = f'Заглушку + щелевой фильтр + НКТ{60}мм {float(khvostEdit)}м + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {float(CreatePZ.column_additional_diametr._value)}мм х ' \
                                f'{CreatePZ.column_additional_wall_thickness._value}мм + НКТ60мм 10м + сбивной клапан с ' \
                                f'ввертышем'
            self.paker_short = f'Заглушку + щелевой фильтр + НКТ{60}мм {float(khvostEdit)}м + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм + НКТ60мм 10м + сбивной клапан с' \
                               f' ввертышем'
            self.dict_nkt = {CreatePZ.nkt_diam: float(CreatePZ.head_column_additional._value),
                             60: int(pakerEdit - float(CreatePZ.head_column_additional._value))}
        elif CreatePZ.column_additional == True and float(
                CreatePZ.column_additional_diametr._value) > 110 and pakerEdit > float(CreatePZ.head_column_additional._value) \
                and swabTrueEditType == False:
            self.paker_select = f'Заглушку + щелевой фильтр + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками ' \
                                f'{khvostEdit}м + пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {float(CreatePZ.column_additional_diametr._value)}мм х ' \
                                f'{CreatePZ.column_additional_wall_thickness._value}мм + НКТ{CreatePZ.nkt_diam}мм со снятыми ' \
                                f'фасками 10м + сбивной клапан с ввертышем'
            self.paker_select = f'Заглушку + щелевой фильтр + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками ' \
                                f'{khvostEdit}м + пакер ПРО-ЯМО-{paker_diametr}мм ' \
                                f' + НКТ{CreatePZ.nkt_diam}мм со снятыми ' \
                                f'фасками 10м + сбивной клапан с ввертышем'
            self.dict_nkt = {CreatePZ.nkt_diam: float(pakerEdit) + float(khvostEdit)}

        elif CreatePZ.nkt_diam == 60:
            self.dict_nkt = {60: float(pakerEdit) + float(khvostEdit)}
        # print(f'компоновка НКТ{pakerEdit, khvostEdit}')
        paker_list = [
            [f' СПО {self.paker_short} до глубины {pakerEdit}м, воронкой до {pakerEdit + khvostEdit}м', None,
             f'Спустить {self.paker_select} на НКТ{CreatePZ.nkt_diam}мм до глубины {pakerEdit}м, воронкой до {pakerEdit + khvostEdit}м'
             f' с замером, шаблонированием шаблоном {CreatePZ.nkt_template}мм. {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(pakerEdit, 1.2)],
            [f'Посадить пакер на глубине {pakerEdit}м', None, f'Посадить пакер на глубине {pakerEdit}м'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [OpressovkaEK.testing_pressure(self, pakerEdit)[1], None,
             OpressovkaEK.testing_pressure(self, pakerEdit)[0],
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
        if depthGaugeEdit == 'Да':
            paker_list.insert(0, ['Заявить 3 глубинных манометра подрядчику по ГИС', None,
                                  f'Заявить 3 глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])
        if QplastEdit == 'ДА':
            paker_list.insert(-2, [f'Насыщение 5м3. Определение Q  '
                                   f'пласт {plast_combo}  при '
                                   f'Р={self.pressure_mode(CreatePZ.expected_P, plast_combo)}атм'
                , None,
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
        return paker_list

    def acid_work(self, swabTrueEditType, acid_proc_edit, khvostEdit, pakerEdit, skv_acid_edit, acid_edit, skv_volume_edit,
                  QplastEdit, skv_proc_edit, plast_combo, acidOilProcEdit, acid_volume_edit, svk_true_edit, dict_nkt, pressure_edit):
        from krs import volume_vn_nkt
        from work_py.opressovka import OpressovkaEK
        from krs import well_volume
        paker_list = []
        swabTrueEditType = False if swabTrueEditType == 'без СКВ' else False
        skv_list = [[f'Определить приемистость при Р-{CreatePZ.max_admissible_pressure._value}атм', None,
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
                     f'тех.жидкостью в объеме {volume_vn_nkt(dict_nkt)}м3 . ',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 0.6],
                    [f'реагирование 2 часа.', None, f'реагирование 2 часа.',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 2],
                    [f'Промывка, Q(повторно)', None, f'Промыть скважину тех.жидкостью круговой циркуляцией обратной промывкой в 1,5 '
                                 f'кратном обьеме. Посадить пакер. Определить приемистость пласта в присутствии '
                                 f'представителя ЦДНГ (составить акт). Сорвать пакер. '
                                 f'При отсутствии приемистости СКВ повторить. При необходимости увеличить приемистость '
                                 f'методом дренирования.',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 0.83 + 0.2 + 0.83 + 0.5 + 0.5]]
        # print(f'СКВ {svk_true_edit}')
        if svk_true_edit == 'Нужно СКВ':
            for row in skv_list:
                paker_list.append(row)

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
        acid_list_1 = [[acid_sel_short, None,
                        f'{acid_sel}'
                        f'ОБЕСПЕЧИТЬ НАЛИЧИЕ У СОСТАВА ВАХТЫ СИЗ ПРИ КИСЛОТНОЙ ОБРАБОТКИ',
                        None, None, None, None, None, None, None,
                        'мастер КРС, УСРСиСТ', None],
                       [None, None,
                        ''.join([f"Закачать кислоту в объеме V={round(volume_vn_nkt(dict_nkt), 1)}м3 (внутренний "
                                 f"объем НКТ)" if acid_volume_edit > volume_vn_nkt(dict_nkt) else f"Закачать кислоту в "
                                                                                                f"объеме {round(acid_volume_edit, 1)}м3, "
                                                                                                f"довести кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) - acid_volume_edit, 1)}м3 "]),
                        None, None, None, None, None, None, None,
                        'мастер КРС', 1.25],
                       [None, None,
                        f'посадить пакер на глубине {pakerEdit}м',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 0.3],
                       [None, None,
                        ''.join(
                            [
                                f'продавить кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) + 0.5, 1)}м3 '
                                f'при давлении не '
                                f'более {CreatePZ.max_admissible_pressure._value}атм. Увеличение давления согласовать'
                                f' с заказчиком' if acid_volume_edit < volume_vn_nkt(
                                    dict_nkt) else f'продавить кислоту оставшейся кислотой в объеме '
                                                   f'{round(acid_volume_edit - volume_vn_nkt(dict_nkt), 1)}м3 и тех жидкостью '
                                                   f'в объеме {round(volume_vn_nkt(dict_nkt) + 0.5, 1)}м3 при давлении '
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
                       [self.flushingDownhole(pakerEdit, khvostEdit, 1)[0], None,
                        self.flushingDownhole(pakerEdit, khvostEdit, 1)[0],
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

            paker_list.append([f'Посадить пакер на {pakerEdit}м. насыщение 5м3', None,
                               f'Посадить пакер на {pakerEdit}м. Произвести насыщение скважины до стабилизации '
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

        swabTrueEditType = self.tabWidget.currentWidget().swabTrueEditType.currentText()
        if swabTrueEditType == 'Нужно освоение':
            CreatePZ.swabTrueEditType = 0
        else:
            CreatePZ.swabTrueEditType = 1
        acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()
        khvostEdit = self.if_None((self.tabWidget.currentWidget().khvostEdit.text()))
        pakerEdit = self.if_None(self.tabWidget.currentWidget().pakerEdit.text())

        skv_volume_edit = float(self.tabWidget.currentWidget().skv_volume_edit.text().replace(',', '.'))
        skv_proc_edit = int(self.tabWidget.currentWidget().skv_proc_edit.text().replace(',', '.'))
        acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
        acid_proc_edit = int(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.'))
        swab_paker = self.if_None(self.tabWidget.currentWidget().swab_pakerEdit.text().replace(',', '.'))
        swab_volume = int(self.tabWidget.currentWidget().swab_volumeEdit.text().replace(',', '.'))
        swabType = str(self.tabWidget.currentWidget().swabTypeCombo.currentText())
        acidOilProcEdit = self.tabWidget.currentWidget().acidOilProcEdit.text()
        pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text())
        plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
        svk_true_edit = str(self.tabWidget.currentWidget().svk_true_edit.currentText())
        skv_acid_edit = str(self.tabWidget.currentWidget().skv_acid_edit.currentText())
        QplastEdit = str(self.tabWidget.currentWidget().QplastEdit.currentText())
        depthGaugeEdit = str(self.tabWidget.currentWidget().depthGaugeCombo.currentText())
        # privyazka = str(self.tabWidget.currentWidget().privyazka.currentText())
        print(khvostEdit, pakerEdit )
        # if (self.if_None(khvostEdit) == 0 or self.if_None(pakerEdit) == 0):
        #     msg = QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
        #     return
        if self.countAcid == 0:
            CreatePZ.khvostEdit = khvostEdit
            CreatePZ.pakerEdit = pakerEdit
            CreatePZ.depthGaugeEdit = depthGaugeEdit
            CreatePZ.swabType = swabType
            CreatePZ.swab_volume = swab_volume
            CreatePZ.swab_paker = swab_paker
            if swabTrueEditType == 'Нужно освоение':
                CreatePZ.swabTrueEditType = 0
            else:
                CreatePZ.swabTrueEditType = 1

            print(f'нужно ли освоение {swabTrueEditType}')
            work_list = self.acidSelect(swabTrueEditType, CreatePZ.khvostEdit, CreatePZ.pakerEdit, depthGaugeEdit, QplastEdit, plast_combo)
            CreatePZ.depthGaugeEdit = depthGaugeEdit

            for row in self.acid_work(swabTrueEditType, acid_proc_edit, CreatePZ.khvostEdit, CreatePZ.pakerEdit, skv_acid_edit, acid_edit,
                                      skv_volume_edit,
                                      QplastEdit, skv_proc_edit, plast_combo, acidOilProcEdit, acid_volume_edit, svk_true_edit,
                                      self.dict_nkt, pressure_edit):
                work_list.append(row)
            self.populate_row(CreatePZ.ins_ind, work_list)
            CreatePZ.ins_ind += len(work_list)

            if swabType == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 0
            elif swabType == 'Задача №2.1.16':  # , 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 1
            elif swabType == 'Задача №2.1.11':  # , 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 2
        elif self.countAcid == 1:

            self.acidSelect(CreatePZ.swabTrueEditType, CreatePZ.khvostEdit, CreatePZ.pakerEdit, CreatePZ.depthGaugeEdit,
                            QplastEdit, plast_combo)
            CreatePZ.pakerEdit = MyWindow.true_set_Paker(self, CreatePZ.pakerEdit)


            work_list = [
                [None, None, f'установить пакер на глубине {pakerEdit}м', None, None, None, None, None, None, None,
                 'мастер КРС', 1.2]]
            for row in self.acid_work(CreatePZ.swabTrueEditType, acid_proc_edit, CreatePZ.khvostEdit, CreatePZ.pakerEdit, skv_acid_edit,
                                      acid_edit,
                                      skv_volume_edit,
                                      QplastEdit, skv_proc_edit, plast_combo, acidOilProcEdit, acid_volume_edit, svk_true_edit,
                                      self.dict_nkt, pressure_edit):
                work_list.append(row)
            self.populate_row(CreatePZ.ins_ind, work_list)
            print(f' индекс строк {CreatePZ.ins_ind}')
            CreatePZ.ins_ind += len(work_list)
            print(f'второй индекс строк {CreatePZ.ins_ind}')
            if swabType == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 0
            elif swabType == 'Задача №2.1.16':  # , 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 1
            elif swabType == 'Задача №2.1.11':  # , 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 2

        elif self.countAcid == 2:
            print(f'ye;yj {CreatePZ.swabTrueEditType}')

            if CreatePZ.swabTrueEditType == 0:
                work_list = []
                swabbing_with_paker = self.swabbing_with_paker(CreatePZ.khvostEdit, CreatePZ.swab_paker, CreatePZ.swabType, CreatePZ.swab_volume)
                for row in swabbing_with_paker:
                    work_list.append(row)
                if CreatePZ.depthGaugeEdit == 'Да':
                    work_list.append([None, None,
                                      f'Подать заявку на вывоз глубинных манометров',
                                      None, None, None, None, None, None, None,
                                      'мастер КРС', None])
            else:
                work_list = [[None, None,
                              f'Поднять компоновку на НКТ с доливом скважины в '
                              f'объеме {round(CreatePZ.pakerEdit * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС',
                              liftingNKT_norm(CreatePZ.pakerEdit, 1.2)]]
            self.populate_row(CreatePZ.ins_ind, work_list)
            # print(f' индекс строк {CreatePZ.ins_ind}')
            CreatePZ.ins_ind += len(work_list)
            # print(f'третья индекс строк {CreatePZ.ins_ind}')

        CreatePZ.pause = False
        self.close()

    def populate_row(self, ins_ind, work_list):
        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700), 160: (701, 800), 180: (801, 1500)}

        for i, row_data in enumerate(work_list):
            row = self.ins_ind + i
            self.table_widget.insertRow(row)

            self.table_widget.setSpan(i + self.ins_ind, 2, 1, 8)
            for column, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                # widget = QtWidgets.QLabel(str())
                # widget.setStyleSheet('border: 0.5px solid black; font: Arial 14px')

                # self.table_widget.setCellWidget(row, column, widget)

                if data is not None:
                    self.table_widget.setItem(row, column, item)

                else:
                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))

                if column == 2:
                    if data is not None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(text_width))

    def del_row_table(self):
        pass
    #     row = self.tableWidget.currentRow()
    #     if row == -1:
    #         msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
    #         return
    #     self.tableWidget.removeRow(row)

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
