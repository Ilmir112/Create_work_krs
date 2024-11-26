from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QWidget, QLabel, QComboBox
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGridLayout, QMessageBox, QInputDialog, QLineEdit, QTabWidget, QPushButton

from main import MyMainWindow


from collections import namedtuple

import data_list
from H2S import calv_h2s
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion


class TabPageSo(TabPageUnion):
    count_plast = []

    def __init__(self, parent=None):
        from work_py.acid_paker import CheckableComboBox
        super().__init__(parent)
        self.labels_category = {}
        self.type_absorbent_label = QLabel('Тип поглотителя')
        self.type_absorbent = QComboBox()
        self.type_absorbent.addItems(['EVASORB марки 121', 'СНПХ-1200', 'ХИМТЕХНО 101 Марка А'])

        self.plast_all = []
        for plast in self.data_well.plast_all[::-1]:
            if plast not in self.plast_all:
                self.plast_all.append(plast)

        for plast in self.data_well.plast_project:
            if plast not in self.plast_all:
                self.plast_all.append(plast)

        self.cat_P_1 = self.data_well.category_pressure
        self.category_h2s_list = self.data_well.category_h2s_list
        self.cat_gaz_f_pr = self.data_well.category_gaz_factor_percent
        self.gaz_f_pr = self.data_well.gaz_factor_percent
        self.h2s_mg = self.data_well.value_h2s_mg

        self.h2s_pr = self.data_well.value_h2s_percent

        self.cat_P_P = self.data_well.category_pressure_well

        self.category_pressure_Label = QLabel('По Рпл')
        self.category_h2s_Label = QLabel('По H2S')
        self.category_h2s2_Label = QLabel('По H2S')
        self.category_Label = QLabel('По газовому фактору')
        self.calc_h2s_Label = QLabel('расчет поглотителя H2S')

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.type_absorbent_label, 2, 1)
        self.grid.addWidget(self.type_absorbent, 3, 1)
        self.grid.addWidget(self.category_pressure_Label, 5, 1)
        self.grid.addWidget(self.category_h2s_Label, 6, 1)
        self.grid.addWidget(self.category_h2s2_Label, 7, 1)
        self.grid.addWidget(self.category_Label, 8, 1)
        self.grid.addWidget(self.calc_h2s_Label, 12, 1)

        n = 1
        work_plast_iter = None
        data_list.number_indez = []
        work_plast = ''
        work_plast_index = 1

        for num in range(len(list(set(self.data_well.category_pressure_well)))):

            plast_index = CheckableComboBox(self)
            try:
                work_plast = self.data_well.plast_work[num]
                work_plast_index = 0
            except:
                if self.data_well.plast_project:
                    work_plast = self.data_well.plast_project[0]
                    work_plast_index = 1

            if num != 0:
                if len(self.data_well.dict_perforation_project) != 0 and \
                        any([plast not in self.data_well.plast_work for plast in self.data_well.plast_project]):

                    if abs(self.cat_P_P[num] - list([self.data_well.dict_perforation_project[
                                                         plast]['давление'] for plast in self.data_well.plast_project][0])[
                        0]) < 1:
                        work_plast = self.data_well.plast_project[0]
                        work_plast_index = 1
                else:
                    plast_index_str = QMessageBox.question(self, 'рабочие пласты',
                                                           f'Есть ли индекс пласта категорийности {num + 1}'
                                                           f'в интервалах перфорации')
                    if plast_index_str == QMessageBox.StandardButton.No:
                        work_plast, ok = QInputDialog.getText(None, 'индекс пласта',
                                                              'Введите индекc пласта вскрываемого')
                        self.data_well.plast_project.append(work_plast)
                        work_plast_index = 1
                    if work_plast not in self.plast_all:
                        self.plast_all.append(work_plast)

            plast_index.combo_box.addItems(self.plast_all)
            aaaa = self.plast_all
            try:
                plast_index.combo_box.setCurrentIndex(self.plast_all.index(work_plast))
            except:
                self.plast_all.append('')
                plast_index.combo_box.setCurrentIndex(self.plast_all.index(work_plast))

            category_pressure_line_edit = QLineEdit(self)
            try:
                category_pressure_line_edit.setText(str(self.ifNone(self.cat_P_1[num])))
            except:
                QMessageBox.warning(self, 'ОШИБКА', 'не вставилось данные по категории')
            pressure_data_edit = QLineEdit(self)
            try:
                pressure_data_edit.setText(str(self.ifNone(self.cat_P_P[num])))
            except:
                pass
            # print(num)
            category_h2s_edit = QLineEdit(self)
            try:
                category_h2s_edit.setText(str(self.ifNone(self.category_h2s_list[num])))
            except:
                pass
            h2s_pr_edit = QLineEdit(self)
            try:
                if str(round(float(str(self.h2s_pr[num]).replace(',', '.')), 3))[-1] == "0":
                    h2s_pr = int(float(self.h2s_pr[num]))
                else:
                    h2s_pr = round(float(str(self.h2s_pr[num]).replace(',', '.')), 4)
                h2s_pr_edit.setText(str(h2s_pr))
            except (IndexError, TypeError):
                pass

            category_h2s2_edit = QLineEdit(self)
            try:
                category_h2s2_edit.setText(str(self.ifNone(self.category_h2s_list[num])))
                h2s_mg_edit = QLineEdit(self)
            except (IndexError, TypeError):
                pass
            try:

                h2s_mg_edit.setText(str(self.h2s_mg[num]))
            except (IndexError, TypeError):

                pass

            category_gf_edit = QLineEdit(self)
            try:
                category_gf_edit.setText(str(self.ifNone(self.cat_gaz_f_pr[num])))
            except (IndexError, TypeError):
                pass
            gaz_f_pr_edit = QLineEdit(self)
            try:
                gaz_f_pr_edit.setText(str(self.ifNone(self.gaz_f_pr[num])))
            except (IndexError, TypeError):
                pass

            units_pressure = QLabel('атм')
            units_h2s_pr = QLabel('%')
            units_h2s_pr.setFixedWidth(150)
            units_h2s_mg = QLabel('мг/дм3')
            units_gaz = QLabel('м3/т')
            isolated_plast = QComboBox(self)
            isolated_plast.addItems(['рабочий', 'планируемый', 'изолирован'])
            isolated_plast.setCurrentIndex(work_plast_index)
            if work_plast_iter is None:
                work_plast_iter = work_plast

            calc_plast_h2s = QLineEdit(self)

            # print(category_h2s_edit.text(), h2s_mg_edit.text(), h2s_pr_edit.text())

            self.grid.addWidget(plast_index, 4, 1 + n, 1, 2)
            self.grid.addWidget(category_pressure_line_edit, 5, 1 + n)
            self.grid.addWidget(category_h2s_edit, 6, 1 + n)
            self.grid.addWidget(category_h2s2_edit, 7, 1 + n)
            self.grid.addWidget(category_gf_edit, 8, 1 + n)
            self.grid.addWidget(isolated_plast, 9, n + 1, 9, n + 1)
            self.grid.addWidget(calc_plast_h2s, 12, n + 1, 12, n + 1)
            self.grid.addWidget(pressure_data_edit, 5, 1 + n + 1)
            self.grid.addWidget(h2s_pr_edit, 6, 1 + n + 1)
            self.grid.addWidget(h2s_mg_edit, 7, 1 + n + 1)
            self.grid.addWidget(gaz_f_pr_edit, 8, 1 + n + 1)
            self.grid.addWidget(units_pressure, 5, 1 + n + 2)

            self.grid.addWidget(units_h2s_pr, 6, 1 + n + 2)
            self.grid.addWidget(units_h2s_mg, 7, 1 + n + 2)
            self.grid.addWidget(units_gaz, 8, 1 + n + 2)

            # Переименование атрибута
            setattr(self, f"{plast_index}_{n}_line", plast_index)
            setattr(self, f"{category_pressure_line_edit}_{n}_line", category_pressure_line_edit)
            setattr(self, f"{pressure_data_edit}_{n}_line", pressure_data_edit)
            setattr(self, f"{category_h2s_edit}_{n}_line", category_h2s_edit)
            setattr(self, f"{category_gf_edit}_{n}_line", category_gf_edit)
            setattr(self, f"{h2s_pr_edit}_{n}_line", h2s_pr_edit)
            setattr(self, f"{h2s_mg_edit}_{n}_line", h2s_mg_edit)
            setattr(self, f"{gaz_f_pr_edit}_{n}_line", gaz_f_pr_edit)
            setattr(self, f"{units_pressure}_{n}_line", units_pressure)
            setattr(self, f"{units_h2s_pr}_{n}_line", units_h2s_pr)
            setattr(self, f"{units_h2s_mg}_{n}_line", units_h2s_mg)
            setattr(self, f"{units_gaz}_{n}_line", units_gaz)
            setattr(self, f"{isolated_plast}_{n}_line", isolated_plast)

            aaa = h2s_mg_edit.text(), h2s_pr_edit.text()
            try:
                calc_plast_h2s.setText(str(calv_h2s(self, category_h2s_edit.text(),
                                                    float(h2s_mg_edit.text()), float(h2s_pr_edit.text()))))
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Приложение не смогла произвести расчет поглотителя H2S, '
                                                    f'Нужно проверить таблицу по категорийности, {e}')

            self.labels_category[n] = (plast_index, category_pressure_line_edit, category_h2s_edit,
                                       category_gf_edit, h2s_pr_edit, h2s_mg_edit, gaz_f_pr_edit,
                                       pressure_data_edit, isolated_plast, calc_plast_h2s)

            data_list.number_indez.append(n)
            n += 3

    def ifNone(self, string):

        if str(string) in ['0', str(None), '-']:
            return 0
        elif str(string).replace('.', '').replace(',', '').isdigit():
            if str(round(float(str(string).replace(',', '.')), 1))[-1] == "0":
                return int(float(string))
            else:
                return round(float(str(string).replace(',', '.')), 4)
        else:
            return str(string)


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSo(parent), 'Проверка корректности данных')


class CategoryWindow(WindowUnion):
    dict_category = {}

    def __init__(self, parent=None):
        super(CategoryWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна

        self.tabWidget = TabWidget(self.data_well)
        self.dict_category = {}

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.add_row_table)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)

    def add_row_table(self):

        # Пересохранение по сереводорода

        cat_P_1 = self.data_well.category_pressure_well
        self.data_well.type_absorbent = self.tabWidget.currentWidget().type_absorbent.currentText()
        plast_index = []
        pressure = namedtuple("pressure", "category data_pressure")
        Data_h2s = namedtuple("Data_h2s", "category data_percent data_mg_l poglot")
        Data_gaz = namedtuple("Data_gaz", "category data")
        aaasse = self.tabWidget.currentWidget().labels_category
        if cat_P_1:
            for index in data_list.number_indez:
                for ind in range(1, 6):
                    if self.ifNum(self.tabWidget.currentWidget().labels_category[index][ind].text()) is False:
                        QMessageBox.warning(self, 'Ошибка', 'ошибка в сохранении данных, не корректные данные ')
                        return

                plast_sel = self.tabWidget.currentWidget().labels_category[index][0].combo_box.currentText()
                if plast_sel == '':
                    QMessageBox.warning(self, 'Выбрать пласты', 'Необходимо выбрать пласты выбрать пласты')
                    return
                for plast in plast_sel.split(', '):
                    plast_index.append(plast)

                    if self.tabWidget.currentWidget().labels_category[index][8].currentText() == 'планируемый':
                        self.data_well.plast_project.append(plast)
                    try:
                        self.dict_category.setdefault(plast, {}).setdefault('по давлению',
                            pressure(int(self.tabWidget.currentWidget().labels_category[index][1].text()),
                                     float(self.tabWidget.currentWidget().labels_category[index][7].text())))

                        self.dict_category.setdefault(plast, {}).setdefault(
                            'по сероводороду', Data_h2s(
                                int(self.tabWidget.currentWidget().labels_category[index][2].text()),
                                float(self.tabWidget.currentWidget().labels_category[index][4].text()),
                                float(self.tabWidget.currentWidget().labels_category[index][5].text()),
                                float(
                                    self.tabWidget.currentWidget().labels_category[index][9].text().replace(',', '.'))))

                        self.dict_category.setdefault(plast, {}).setdefault(
                            'по газовому фактору', Data_gaz(
                                int(self.tabWidget.currentWidget().labels_category[index][3].text()),
                                float(self.tabWidget.currentWidget().labels_category[index][6].text())))

                        self.dict_category.setdefault(plast, {}).setdefault(
                            'отключение', self.tabWidget.currentWidget().labels_category[index][8].currentText())

                        self.data_well.dict_category = self.dict_category
                        data_list.pause = False

                    except Exception as e:
                        QMessageBox.warning(self, 'Ошибка', f"Ошибка сохранения данных по категории {e}")
                        return

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