import json
import well_data


import psycopg2
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton
from datetime import datetime


from krs import TabPageGno, GnoWindow
from well_data import well_area, well_number
from work_py.alone_oreration import lifting_unit, weigth_pipe, volume_pod_NKT, pvo_gno, volume_jamming_well
from work_py.mkp import mkp_revision_1_kateg
from work_py.rationingKRS import liftingNKT_norm


class TabPageDp(QWidget):
    def __init__(self, work_plan):
        super().__init__()
        self.work_plan = work_plan
        self.table_name = well_data.well_number._value + well_data.well_area._value

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')

        self.fluid_label = QLabel("уд.вес жидкости глушения", self)
        self.fluid_edit = QLineEdit(self)
        # if well_data.fluid_work == '':
        #     self.fluid_edit.setText(f'{TabPageGno.calc_fluid(self.work_plan, well_data.current_bottom)}')
        # else:
        #     self.fluid_edit.setText(f'{well_data.fluid_work}')
        table_list = self.get_tables_starting_with(self.table_name)

        self.work_label = QLabel("Ранее проведенные работы:", self)
        self.work_edit = QLineEdit(self)

        grid = QGridLayout(self)
        grid.addWidget(self.current_bottom_label, 4, 4)
        grid.addWidget(self.current_bottom_edit, 5, 4)
        grid.addWidget(self.fluid_label, 4, 5)
        grid.addWidget(self.fluid_edit, 5, 5)
        grid.addWidget(self.work_label, 6, 6, 2, 3)
        grid.addWidget(self.work_edit, 8, 6, 2, 3)

        if well_data.data_in_base:
            self.table_in_base_label = QLabel('данные в таблице')
            self.table_in_base_combo = QComboBox()
            print(table_list, type(table_list))

            self.table_in_base_combo.addItems(table_list)

            self.index_change_label = QLabel('пункт после которого происходят изменения')
            self.index_change_line = QLineEdit(self)
            grid.addWidget(self.table_in_base_label, 4, 7)
            grid.addWidget(self.table_in_base_combo, 5, 7)
            grid.addWidget(self.index_change_label, 4, 8)
            grid.addWidget(self.index_change_line, 5, 8)

            self.table_in_base_combo.currentTextChanged.connect(self.update_table_in_base_combo)
            self.index_change_line.textChanged.connect(self.update_table_in_base_combo)

    def update_table_in_base_combo(self):
        index_change_line = self.index_change_line.text()
        table_in_base_combo = self.table_in_base_combo.currentText()

        if index_change_line != '':
            index_change_line = int(float(index_change_line))
            DopPlanWindow.extraction_data(self, table_in_base_combo, index_change_line)
            self.current_bottom_edit.setText(str(well_data.current_bottom))
            print(well_data.fluid_work)
            self.fluid_edit.setText(str(well_data.fluid_work))



    def get_tables_starting_with(self, prefix):
        """
        Возвращает список таблиц, имена которых начинаются с заданного префикса.
        """
        conn = psycopg2.connect(**well_data.postgres_conn_work_well)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name LIKE %s
      """, (prefix + '%',))

        tables = [row[0] for row in cursor.fetchall()]
        tables.insert(0, '')

        cursor.close()
        return tables





class TabWidget(QTabWidget):
    def __init__(self, work_plan):
        super().__init__()
        self.addTab(TabPageDp(work_plan), 'Дополнительный план работ')


class DopPlanWindow(QMainWindow):
    def __init__(self, ins_ind, table_widget, work_plan, parent=None):

        super(DopPlanWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.work_plan = work_plan
        self.tabWidget = TabWidget(self.work_plan)

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        from main import MyWindow
        fluid = self.tabWidget.currentWidget().fluid_edit.text()
        current_bottom = self.tabWidget.currentWidget().current_bottom_edit.text()
        if current_bottom != '':
            current_bottom = round(float(current_bottom.replace(',', '.')), 1)

        work_earlier = self.tabWidget.currentWidget().work_edit.text()


        if well_data.data_in_base:
            fluid = self.tabWidget.currentWidget().fluid_edit.text()

            table_in_base_combo = str(self.tabWidget.currentWidget().table_in_base_combo.currentText())
            index_change_line = self.tabWidget.currentWidget().index_change_line.text()
            if index_change_line != '':
                index_change_line = int(float(index_change_line))

            else:
                mes = QMessageBox.critical(self, 'пункт', 'Необходимо выбрать пункт плана работ')
                return
            if table_in_base_combo == '':
                mes = QMessageBox.critical(self, 'База данных', 'Необходимо выбрать план работ')
                return

            self.extraction_data(table_in_base_combo, index_change_line)



        if current_bottom == '' or fluid == '' or work_earlier == '':
            # print(current_bottom, fluid, work_earlier)
            mes = QMessageBox.critical(self, 'Забой', 'не все значения введены')
            return

        if current_bottom > well_data.bottomhole_drill._value:
            mes = QMessageBox.critical(self, 'Забой', 'Текущий забой больше пробуренного забоя')
            return
        if (0.87 <= float(fluid[:3]) <= 1.64) == False:
            mes = QMessageBox.critical(self, 'рабочая жидкость',
                                       'уд. вес рабочей жидкости не может быть меньше 0,87 и больше 1,64')
            return

        if 'г/см3' not in fluid:
            mes = QMessageBox.critical(self, 'удвес', 'нужно добавить значение "г/см3" в уд.вес')
            return
        well_data.fluid_work = fluid
        well_data.current_bottom = current_bottom

        work_list = self.work_list(work_earlier)
        MyWindow.populate_row(self, self.ins_ind + 2, work_list, self.table_widget, self.work_plan)
        well_data.pause = False

        if str(fluid) not in str(well_data.fluid_work):
            well_data.fluid_work, well_data.fluid_work_short = GnoWindow.calc_work_fluid(self, fluid)

    def extraction_data(self, table_name, paragraph_row):
        try:
            # Устанавливаем соединение с базой данных
            conn1 = psycopg2.connect(**well_data.postgres_conn_work_well)

            cursor1 = conn1.cursor()

            # Проверяем наличие таблицы с определенным именем
            result_table = 0
            number_dp = int(well_data.number_dp) - 1
            if well_data.work_plan in ['krs', 'plan_change']:
                work_plan = 'krs'

                table_name = f'{well_data.well_number._value + well_data.well_area._value + work_plan}'

                # print(cursor1.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables").fetchall())
                cursor1.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')")
                result_table = cursor1.fetchone()

            elif well_data.work_plan == f'dop_plan':
                if number_dp == 0:
                    cursor1.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables "
                                    f"WHERE table_name = '{table_name}')")
                    print(f'имя таблицы в {table_name}')
                    result_table = cursor1.fetchone()
                    print(result_table)

            if result_table[0]:
                well_data.data_in_base = True
                cursor2 = conn1.cursor()

                cursor2.execute(f'SELECT * FROM "{table_name}"')
                result = cursor2.fetchall()
                if well_data.work_plan == 'dop_plan':
                    DopPlanWindow.insert_data_dop_plan(self, result, paragraph_row)
                elif well_data.work_plan == 'plan_change':
                    DopPlanWindow.insert_data_plan(self, result)
                well_data.data_well_is_True = True

            else:
                well_data.data_in_base = False
                mes = QMessageBox.warning(self, 'Проверка наличия таблицы в базе данных',
                                          f"Таблицы '{table_name}' нет в базе данных.")


        except psycopg2.Error as e:
            # Выведите сообщение об ошибке
            mes = QMessageBox.warning(None, 'Ошибка', 'Ошибка подключения к базе данных,')
        finally:
            # Закройте курсор и соединение
            if cursor1:
                cursor1.close()
            if conn1:
                conn1.close()


    def insert_data_dop_plan(self, result, paragraph_row):
        try:
            paragraph_row = paragraph_row
        except:
            paragraph_row = 1
        well_data.current_bottom = result[paragraph_row][1]

        well_data.dict_perforation = json.loads(result[paragraph_row][2])
        well_data.plast_all = json.loads(result[paragraph_row][3])
        well_data.plast_work = json.loads(result[paragraph_row][4])
        well_data.leakage = json.loads(result[paragraph_row][5])
        if result[paragraph_row][6] == 0:
            well_data.column_additional = True
        else:
            well_data.column_additional = False


        well_data.fluid_work = result[paragraph_row][7]

        well_data.category_pressuar = result[paragraph_row][8]
        well_data.category_h2s = result[paragraph_row][9]
        well_data.category_gf = result[paragraph_row][10]
        well_data.template_depth = result[paragraph_row][11]

        well_data.skm_list = json.loads(result[paragraph_row][12])

        well_data.problemWithEk_depth = result[paragraph_row][13]
        well_data.problemWithEk_diametr = result[paragraph_row][14]
        well_data.dict_perforation_short = json.loads(result[paragraph_row][2])

    def insert_data_plan(self, result):
        well_data.data_list = []
        for row in result:
            data_list = []
            for index, data in enumerate(row):
                if index == 6:
                    print(data)
                    if data == 'false':
                        data = False
                    else:
                        data = True
                data_list.append(data)
            well_data.data_list.append(data_list)



    def work_list(self, work_earlier):
        krs_begin = [[None, None,
             f' Ранее проведенные работ: \n {work_earlier}',
             None, None, None, None, None, None, None,
             'Мастер КРС', None]]
        return krs_begin