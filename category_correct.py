from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtGui import QRegExpValidator, QColor, QPalette
from collections import namedtuple
import re


class FloatLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(FloatLineEdit, self).__init__(parent)

        # Устанавливаем валидатор для проверки на float

        reg = QRegExp("[0-9.отсут]*")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.setValidator(pValidator)

    def focusOutEvent(self, event):
        # При потере фокуса проверяем, является ли текст float
        if self.validator().validate(self.text(), 0)[0] != QValidator.Acceptable:
            # Если текст не является числом, меняем цвет фона на красный
            palette = self.palette()
            palette.setColor(QPalette.Base, QColor(Qt.red))
            self.setPalette(palette)
        else:
            # Если текст является числом, возвращаем цвет фона по умолчанию
            self.setPalette(self.parentWidget().palette())


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        from open_pz import CreatePZ
        self.labels_category = {}

        self.plast_all = []
        for plast in CreatePZ.plast_all:
            self.plast_all.append(plast)

        for plast in CreatePZ.plast_project:
            self.plast_all.append(plast)

        print(f'пласты {self.plast_all}')
        self.cat_P_1 = CreatePZ.cat_P_1
        self.cat_H2S_list = CreatePZ.cat_H2S_list
        self.cat_gaz_f_pr = CreatePZ.cat_gaz_f_pr
        self.gaz_f_pr = CreatePZ.gaz_f_pr
        self.H2S_mg = CreatePZ.H2S_mg
        self.H2S_pr = CreatePZ.H2S_pr
        self.cat_P_P = CreatePZ.cat_P_P

        self.category_pressuar_Label = QLabel('По Рпл')
        self.category_h2s_Label = QLabel('По H2S')
        self.category_h2s2_Label = QLabel('По H2S')
        self.category_gf_Label = QLabel('По газовому фактору')

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.category_pressuar_Label, 5, 1)
        self.grid.addWidget(self.category_h2s_Label, 6, 1)
        self.grid.addWidget(self.category_h2s2_Label, 7, 1)
        self.grid.addWidget(self.category_gf_Label, 8, 1)

        n = 1
        CreatePZ.number_indez = []
        print(f'строки {list(set(CreatePZ.cat_P_P))}')

        for num in range(len(list(set(CreatePZ.cat_P_P)))):

            plast_index = QComboBox(self)
            plast_index.addItems(self.plast_all)
            work_plast = CreatePZ.plast_work[0]
            work_plast_index = 0
            if CreatePZ.dict_perforation_project:
                if abs(self.cat_P_P[num] - list([CreatePZ.dict_perforation_project[plast]['давление'] for plast in CreatePZ.plast_project][0])[0]) < 1:
                    work_plast = CreatePZ.plast_project[0]
                    work_plast_index = 1



            print(f'пласт {work_plast}')
            plast_index.setCurrentIndex(self.plast_all.index(work_plast))

            category_pressuar_line_edit = QLineEdit(self)
            category_pressuar_line_edit.setText(str(self.ifNone(self.cat_P_1[num])))

            pressuar_data_edit = QLineEdit(self)
            pressuar_data_edit.setText(str(self.ifNone(self.cat_P_P[num])))

            category_h2s_edit = QLineEdit(self)
            category_h2s_edit.setText(str(self.ifNone(self.cat_H2S_list[num])))
            H2S_pr_edit = QLineEdit(self)
            H2S_pr_edit.setText(str(self.ifNone(self.H2S_pr[num])))

            category_h2s2_edit = QLineEdit(self)
            category_h2s2_edit.setText(str(self.ifNone(self.cat_H2S_list[num])))
            H2S_mg_edit = QLineEdit(self)
            H2S_mg_edit.setText(str(self.ifNone(self.H2S_mg[num])))

            category_gf_edit = QLineEdit(self)
            category_gf_edit.setText(str(self.ifNone(self.cat_gaz_f_pr[num])))
            gaz_f_pr_edit = QLineEdit(self)
            gaz_f_pr_edit.setText(str(self.ifNone(self.gaz_f_pr[num])))
            units_pressuar = QLabel('атм')
            units_h2s_pr = QLabel('%')
            units_h2s_pr.setFixedWidth(150)
            units_h2s_mg = QLabel('мг/дм3')
            units_gaz = QLabel('м3/т')
            isolated_plast = QComboBox(self)
            isolated_plast.addItems(['рабочий', 'планируемый', 'изолирован'])
            isolated_plast.setCurrentIndex(work_plast_index)

            self.grid.addWidget(plast_index, 4, 1 + n)
            self.grid.addWidget(category_pressuar_line_edit, 5, 1 + n)
            self.grid.addWidget(category_h2s_edit, 6, 1 + n)
            self.grid.addWidget(category_h2s2_edit, 7, 1 + n)
            self.grid.addWidget(category_gf_edit, 8, 1 + n)
            self.grid.addWidget(isolated_plast, 9, n + 1, 9, n + 1)
            self.grid.addWidget(pressuar_data_edit, 5, 1 + n + 1)
            self.grid.addWidget(H2S_pr_edit, 6, 1 + n + 1)
            self.grid.addWidget(H2S_mg_edit, 7, 1 + n + 1)
            self.grid.addWidget(gaz_f_pr_edit, 8, 1 + n + 1)
            self.grid.addWidget(units_pressuar, 5, 1 + n + 2)

            self.grid.addWidget(units_h2s_pr, 6, 1 + n + 2)
            self.grid.addWidget(units_h2s_mg, 7, 1 + n + 2)
            self.grid.addWidget(units_gaz, 8, 1 + n + 2)

            # Переименование атрибута
            setattr(self, f"{plast_index}_{n}_line", plast_index)
            setattr(self, f"{category_pressuar_line_edit}_{n}_line", category_pressuar_line_edit)
            setattr(self, f"{pressuar_data_edit}_{n}_line", pressuar_data_edit)
            setattr(self, f"{category_h2s_edit}_{n}_line", category_h2s_edit)
            setattr(self, f"{category_gf_edit}_{n}_line", category_gf_edit)
            setattr(self, f"{H2S_pr_edit}_{n}_line", H2S_pr_edit)
            setattr(self, f"{H2S_mg_edit}_{n}_line", H2S_mg_edit)
            setattr(self, f"{gaz_f_pr_edit}_{n}_line", gaz_f_pr_edit)
            setattr(self, f"{units_pressuar}_{n}_line", units_pressuar)
            setattr(self, f"{units_h2s_pr}_{n}_line", units_h2s_pr)
            setattr(self, f"{units_h2s_mg}_{n}_line", units_h2s_mg)
            setattr(self, f"{units_gaz}_{n}_line", units_gaz)
            setattr(self, f"{isolated_plast}_{n}_line", isolated_plast)

            self.labels_category[n] = (plast_index, category_pressuar_line_edit, category_h2s_edit,
                                       category_gf_edit, H2S_pr_edit, H2S_mg_edit, gaz_f_pr_edit,
                                       pressuar_data_edit, isolated_plast)

            CreatePZ.number_indez.append(n)
            n += 3

    def ifNone(self, string):

        if str(string) in ['0', str(None), '-']:
            return 'отсут'
        elif str(string).replace('.', '').replace(',', '').isdigit():

            # print(str(round(float(string), 1))[-1] == '0', int(string), float(string))
            return int(float(string)) if str(round(float(str(string).replace(',', '.')), 1))[-1] == "0" else \
                round(float(str(string).replace(',', '.')), 1)
        else:
            return str(string)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Проверка корректности данных')


class CategoryWindow(QMainWindow):
    dict_category = {}

    def __init__(self, parent=None):
        super(CategoryWindow, self).__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна
        self.tabWidget = TabWidget()
        self.dict_category = {}

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.addRowTable)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)

    def addRowTable(self):
        from open_pz import CreatePZ
        # Пересохранение по сереводорода

        cat_P_1 = CreatePZ.cat_P_1

        plast_index = []
        Pressuar = namedtuple("Pressuar", "category data_pressuar")
        Data_h2s = namedtuple("Data_h2s", "category data_procent data_mg_l")
        Data_gaz = namedtuple("Data_gaz", "category data")
        if cat_P_1:
            for index in CreatePZ.number_indez:
                for ind in range(1, 6):
                    if self.ifNum(self.tabWidget.currentWidget().labels_category[index][ind].text()) is False:
                        mes = QMessageBox.warning(self, 'Ошибка', 'ошибка в сохранении данных, не корректные данные ')
                        return

                plast = self.tabWidget.currentWidget().labels_category[index][0].currentText()
                plast_index.append(plast)

                CategoryWindow.dict_category.setdefault(plast, {}).setdefault(
                    'по давлению',
                    Pressuar(int(self.tabWidget.currentWidget().labels_category[index][1].text()),
                        float(self.tabWidget.currentWidget().labels_category[index][7].text())))

                CategoryWindow.dict_category.setdefault(plast, {}).setdefault(
                    'по сероводороду', Data_h2s(
                        int(self.tabWidget.currentWidget().labels_category[index][2].text()),
                        float(self.tabWidget.currentWidget().labels_category[index][4].text()),
                        float(self.tabWidget.currentWidget().labels_category[index][5].text())))

                CategoryWindow.dict_category.setdefault(plast, {}).setdefault(
                    'по газовому фактору', Data_gaz(
                        int(self.tabWidget.currentWidget().labels_category[index][3].text()),
                        float(self.tabWidget.currentWidget().labels_category[index][6].text())))

                CategoryWindow.dict_category.setdefault(plast, {}).setdefault(
                    'отключение', self.tabWidget.currentWidget().labels_category[index][8].currentText())

        CreatePZ.pause = False
        self.close()


    def ifNum(self, string):
        # метод для проверки и преобразования введенных значений
        if str(string) == "['0']":
            return False
        elif str(string) == 'отсут':
            return True
        elif str(string).replace('.', '').replace(',', '').isdigit():
            if float(string.replace(',', '.')) < 5000:
                return True
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = CategoryWindow()
    QTimer.singleShot(2000, CategoryWindow)
    # window.show()
    app.exec_()
