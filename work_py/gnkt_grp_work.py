from PyQt5.QtGui import QIntValidator, QDoubleValidator

import block_name

import well_data

from datetime import datetime

from data_base.config_base import connect_to_database, connection_to_database, GnktDatabaseWell

from main import MyMainWindow

from PyQt5.QtWidgets import QInputDialog, QTabWidget, QWidget, QApplication, QLabel, \
    QLineEdit, QGridLayout, QComboBox, QPushButton, QMessageBox
from openpyxl.utils import get_column_letter
from gnkt_data.gnkt_data import gnkt_1, gnkt_2, gnkt_dict, read_database_gnkt
from block_name import razdel_1
from openpyxl.styles import PatternFill, Font, Alignment

from work_py.acid_paker import CheckableComboBox
from work_py.alone_oreration import well_volume


class TabPageGnkt(QWidget):
    def __init__(self):
        super().__init__()

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0, 8000, 1)

        self.init_gnkt()

    def init_gnkt(self):
        self.gnkt_number_label = QLabel('Номер флота ГНКТ')
        self.gnkt_number_combo = QComboBox(self)
        self.gnkt_number_combo.addItems(gnkt_dict["Ойл-сервис"])
        if self.gnkt_number_combo.currentText() == 'ГНКТ №1':
            self.gnkt = gnkt_1
        elif self.gnkt_number_combo.currentText() == 'ГНКТ №2':
            self.gnkt = gnkt_2

        self.lenght_gnkt_label = QLabel('длина ГНКТ')
        self.lenght_gnkt_edit = QLineEdit(self)

        self.iznos_gnkt_label = QLabel('Износ трубы')
        self.iznos_gnkt_edit = QLineEdit(self)

        self.pvo_number_label = QLabel('Номер ПВО')
        self.pvo_number_edit = QLineEdit(self)

        self.pipe_mileage_label = QLabel('Пробег трубы')
        self.pipe_mileage_edit = QLineEdit(self)

        self.previous_well_label = QLabel('Предыдущая скважина')
        self.previous_well_combo = QComboBox(self)

        self.current_bottom_label = QLabel('необходимый текущий забой')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')

        self.fluid_label = QLabel("уд.вес жидкости глушения", self)
        self.fluid_edit = QLineEdit(self)
        if well_data.work_plan == 'gnkt_opz':
            self.fluid_edit.setText('1.18')
        else:
            self.fluid_edit.setText('1.01')

        self.distance_pntzh_label = QLabel('Расстояние до ПНТЖ')
        self.distance_pntzh_line = QLineEdit(self)
        self.distance_pntzh_line.setValidator(self.validator_int)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.gnkt_number_label, 0, 2, 1, 5)
        self.grid.addWidget(self.gnkt_number_combo, 1, 2, 1, 5)
        self.grid.addWidget(self.lenght_gnkt_label, 2, 3)
        self.grid.addWidget(self.lenght_gnkt_edit, 3, 3)
        self.grid.addWidget(self.iznos_gnkt_label, 2, 4)
        self.grid.addWidget(self.iznos_gnkt_edit, 3, 4)

        self.grid.addWidget(self.pipe_mileage_label, 2, 5)
        self.grid.addWidget(self.pipe_mileage_edit, 3, 5)

        self.grid.addWidget(self.pvo_number_label, 2, 6)
        self.grid.addWidget(self.pvo_number_edit, 3, 6)

        self.grid.addWidget(self.previous_well_label, 2, 7)
        self.grid.addWidget(self.previous_well_combo, 3, 7)

        self.grid.addWidget(self.current_bottom_label, 4, 2)
        self.grid.addWidget(self.current_bottom_edit, 5, 2)
        self.grid.addWidget(self.fluid_label, 4, 3)
        self.grid.addWidget(self.fluid_edit, 5, 3)
        self.grid.addWidget(self.distance_pntzh_label, 4, 5)
        self.grid.addWidget(self.distance_pntzh_line, 5, 5)

        self.acids_work_label = QLabel('Проведение ОПЗ')
        self.acids_work_combo = QComboBox(self)
        self.acids_work_combo.addItems(['Нет', 'Да'])

        if well_data.work_plan == 'gnkt_after_grp':

            self.osvoenie_label = QLabel('Необходимость освоения')
            self.osvoenie_combo = QComboBox(self)
            self.osvoenie_combo.addItems(['', 'Да', 'Нет'])

            self.grid.addWidget(self.osvoenie_label, 4, 4)
            self.grid.addWidget(self.osvoenie_combo, 5, 4)
            self.grid.addWidget(self.acids_work_label, 6, 2)
            self.grid.addWidget(self.acids_work_combo, 7, 2)

            self.acids_work_combo.setCurrentIndex(2)
        elif well_data.work_plan == 'gnkt_frez':
            self.need_frez_port_label = QLabel('Необходимость фрезерования портов')
            self.need_frez_port_combo = QComboBox(self)
            self.need_frez_port_combo.addItems(['', 'Нет', 'Да'])
            self.grid.addWidget(self.need_frez_port_label, 4, 4)
            self.grid.addWidget(self.need_frez_port_combo, 5, 4)
            self.grid.addWidget(self.acids_work_label, 6, 2)
            self.grid.addWidget(self.acids_work_combo, 7, 2)
        else:
            self.acids_work_label.setParent(None)
            self.acids_work_combo.setParent(None)

        self.acids_work_combo.currentTextChanged.connect(self.update_acids_work)
        self.gnkt_number_combo.currentTextChanged.connect(self.update_number_gnkt)
        self.previous_well_combo.currentTextChanged.connect(self.update_data_gnkt)

    def update_acids_work(self, index):
        if index == 'Нет':
            self.acids_type_label.setParent(None)
            self.acid_edit.setParent(None)
            self.acid_volume_label.setParent(None)
            self.acid_volume_edit.setParent(None)
            self.acid_proc_label.setParent(None)
            self.acid_proc_edit.setParent(None)
            self.pressure_Label.setParent(None)
            self.pressure_edit.setParent(None)
            self.roof_label.setParent(None)
            self.roof_edit.setParent(None)

            self.sole_label.setParent(None)
            self.sole_edit.setParent(None)

            self.plast_label.setParent(None)
            self.plast_combo.setParent(None)

        elif index == 'Да':
            self.acids_type_label = QLabel('Вид кислоты')
            self.acid_edit = QComboBox(self)
            self.acid_edit.addItems(['Лимонная кислота', 'HCl', 'HF', 'vt'])
            self.acid_volume_label = QLabel("Объем кислотной обработки", self)
            self.acid_volume_edit = QLineEdit(self)
            self.acid_volume_edit.setValidator(self.validator_float)
            self.acid_volume_edit.setText("3")
            self.acid_volume_edit.setClearButtonEnabled(True)
            self.acid_proc_label = QLabel("Концентрация кислоты", self)
            self.acid_proc_edit = QLineEdit(self)
            self.acid_proc_edit.setText('15')
            self.acid_proc_edit.setClearButtonEnabled(True)
            self.acid_proc_edit.setValidator(self.validator_int)
            self.pressure_Label = QLabel("Давление закачки", self)
            self.pressure_edit = QLineEdit(self)
            self.pressure_edit.setText(f'{well_data.max_admissible_pressure._value}')
            self.pressure_edit.setValidator(self.validator_int)

            self.roof_label = QLabel("кровля пласта", self)
            self.roof_edit = QLineEdit(self)
            self.roof_edit.setText(f'{well_data.perforation_roof}')
            self.roof_edit.setValidator(self.validator_float)

            self.sole_label = QLabel("подошва пласта", self)
            self.sole_edit = QLineEdit(self)
            self.sole_edit.setText(f'{well_data.perforation_sole}')
            self.sole_edit.setValidator(self.validator_float)
            plast_work = ['']
            plast_work.extend(well_data.plast_work)

            self.plast_label = QLabel("Выбор пласта", self)
            self.plast_combo = CheckableComboBox(self)
            self.plast_combo.combo_box.addItems(plast_work)

            self.grid.addWidget(self.plast_label, 8, 2)
            self.grid.addWidget(self.plast_combo, 9, 2)
            self.grid.addWidget(self.roof_label, 8, 3)
            self.grid.addWidget(self.roof_edit, 9, 3)
            self.grid.addWidget(self.sole_label, 8, 4)
            self.grid.addWidget(self.sole_edit, 9, 4)

            self.grid.addWidget(self.acids_type_label, 6, 3)
            self.grid.addWidget(self.acid_edit, 7, 3)
            self.grid.addWidget(self.acid_volume_label, 6, 4)
            self.grid.addWidget(self.acid_volume_edit, 7, 4)
            self.grid.addWidget(self.acid_proc_label, 6, 5)
            self.grid.addWidget(self.acid_proc_edit, 7, 5)
            self.grid.addWidget(self.pressure_Label, 6, 6)
            self.grid.addWidget(self.pressure_edit, 7, 6)

    def update_data_gnkt(self):
        previus_well = self.previous_well_combo.currentText()
        try:
            if previus_well:
                db = connection_to_database(well_data.DB_NAME_GNKT)
                data_gnkt = GnktDatabaseWell(db)

                if 'ойл-сервис' in well_data.contractor.lower():
                    contractor = 'oil_service'

                result_gnkt = data_gnkt.update_data_gnkt(contractor, previus_well)

                self.lenght_gnkt_edit.setText(str(result_gnkt[3]))
                self.iznos_gnkt_edit.setText(str(result_gnkt[5]))
                self.pipe_mileage_edit.setText(str(result_gnkt[6]))
                self.pvo_number_edit.setText(str(result_gnkt[10]))


        except Exception as e:
            print(f'Ошибка  с базой ГНКТ {e}')

    def update_number_gnkt(self, gnkt_number):
        if gnkt_number != '':
            well_previus_list = read_database_gnkt(well_data.contractor, gnkt_number)

            self.previous_well_combo.clear()
            self.previous_well_combo.addItems(list(map(str, well_previus_list)))


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPageGnkt(), 'Данные по ГНКТ')


class GnktModel(MyMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.tabWidget = TabWidget()

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def insert_image_schema(self, ws):

        if well_data.paker_do["do"] != 0:
            coordinate_nkt_with_paker = 'F6'
            self.insert_image(ws, f'{well_data.path_image}imageFiles/schema_well/НКТ с пакером.png',
                              coordinate_nkt_with_paker, 100, 510)
        elif well_data.dict_nkt:
            coordinate_nkt_with_voronka = 'F6'
            self.insert_image(ws, f'{well_data.path_image}imageFiles/schema_well/НКТ с воронкой.png',
                              coordinate_nkt_with_voronka, 70, 470)

        if self.work_plan in ['gnkt_bopz']:
            coordinate = 'F65'
            self.insert_image(ws, f'{well_data.path_image}imageFiles/schema_well/angle_well.png',
                              coordinate, 265, 373)

        elif self.work_plan in ['gnkt_after_grp', 'gnkt_opz']:
            coordinate_propant = 'F43'
            if self.work_plan in ['gnkt_after_grp']:
                self.insert_image(ws, f'{well_data.path_image}imageFiles/schema_well/пропант.png',
                                  coordinate_propant, 90, 500)

            n = 0
            m = 0
            for plast, interval in well_data.img_pvr_list:
                for roof_plast, sole_plast in interval:
                    count_interval = well_data.dict_perforation[plast]['счет_объединение']

                    ws.merge_cells(start_column=23, start_row=27 + m,
                                   end_column=23, end_row=27 + count_interval + m - 1)
                    ws.merge_cells(start_column=22, start_row=27 + m,
                                   end_column=22, end_row=27 + count_interval + m - 1)
                    ws.merge_cells(start_column=21, start_row=27 + m,
                                   end_column=21, end_row=27 + count_interval + m - 1)
                    m += count_interval

                    try:
                        if roof_plast > well_data.depth_fond_paker_do["do"] and roof_plast < well_data.current_bottom:
                            interval_str = f'{plast} \n {roof_plast}-{sole_plast}'
                            coordinate_pvr = f'F{43 + n}'

                            ws.cell(row=43 + n, column=10).value = interval_str
                            ws.merge_cells(start_column=10, start_row=43 + n,
                                           end_column=12, end_row=43 + n + 2)
                            ws.cell(row=43 + n, column=10).font = Font(name='Arial', size=12, bold=True)
                            ws.cell(row=43 + n, column=10).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                                 vertical='center')
                            n += 3
                            self.insert_image(ws, f'{well_data.path_image}imageFiles/schema_well/ПВР.png',
                                              coordinate_pvr, 85, 40)
                    except:
                        QMessageBox.critical(self,
                                             'Ошибка', f'программа не смогла вставить интервал перфорации в схему'
                                                       f'{roof_plast}-{sole_plast}')

            coordinate_voln = f'E18'
            self.insert_image(ws,
                              f'{well_data.path_image}imageFiles/schema_well/переход.png',
                              coordinate_voln, 150, 60)

    def count_row_height(self, ws2, work_list, sheet_name):

        from openpyxl.utils.cell import range_boundaries, get_column_letter

        colWidth = [2.85546875, 14.42578125, 16.140625, 22.85546875, 17.140625, 14.42578125, 13.0, 13.0, 17.0,
                    14.42578125, 13.0, 21, 12.140625, None]

        text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 110: (301, 400), 120: (401, 500),
                           130: (501, 600), 150: (601, 700), 170: (701, 800), 190: (801, 900), 230: (901, 1500)}

        boundaries_dict = {}

        for ind, _range in enumerate(ws2.merged_cells.ranges):
            boundaries_dict[ind] = range_boundaries(str(_range))

        for key, value in boundaries_dict.items():
            ws2.unmerge_cells(start_column=value[0], start_row=value[1],
                              end_column=value[2], end_row=value[3])

        ins_ind = 1

        for i in range(1, len(work_list) + 1):  # Добавлением работ
            if sheet_name == 'Ход работ':
                if len(str(work_list[i - 1][1])) <= 3 and str(work_list[i - 1][1]) != '№' and \
                        str(work_list[i - 1][1]) != 'п/п':  # Нумерация
                    work_list[i - 1][1] = str(ins_ind)
                    ins_ind += 1
                elif str(work_list[i - 1][1]) == 'п/п':
                    ins_ind = 1

            for j in range(1, 13):
                cell = ws2.cell(row=i, column=j)

                if cell and str(cell) != str(work_list[i - 1][j - 1]):
                    if str(work_list[i - 1][j - 1]).replace('.', '').isdigit() and \
                            str(work_list[i - 1][j - 1]).count('.') != 2:
                        cell.value = str(work_list[i - 1][j - 1]).replace('.', ',')

                    else:
                        cell.value = work_list[i - 1][j - 1]

        # print(merged_cells_dict)
        if sheet_name != 'Ход работ':
            for key, value in boundaries_dict.items():
                # print(value)
                ws2.merge_cells(start_column=value[0], start_row=value[1],
                                end_column=value[2], end_row=value[3])
            if sheet_name == "Титульник":
                for i, row_data in enumerate(work_list):
                    # print(f'gghhg {work_list[i][2]}')
                    for column, data in enumerate(row_data):
                        if i < 2:
                            ws2.cell(row=i + 1, column=column + 1).alignment = Alignment(horizontal='left',
                                                                                         vertical='center')

            elif sheet_name == 'СХЕМА' and self.work_plan != 'gnkt_frez':
                self.insert_image_schema(ws2)


        elif sheet_name == 'Ход работ':
            for i, row_data in enumerate(work_list):
                # print(f'gghhg {work_list[i][2]}')
                for column, data in enumerate(row_data):
                    if column == 2:
                        if not data is None:
                            text = data
                            for key, value in text_width_dict.items():
                                if value[0] <= len(text) <= value[1]:
                                    ws2.row_dimensions[i + 1].height = int(key)
                    elif column == 1:
                        if not data is None:
                            text = data
                            # print(text)
                            for key, value in text_width_dict.items():
                                if value[0] <= len(text) <= value[1]:
                                    ws2.row_dimensions[i + 1].height = int(key)
                    if column != 0:
                        ws2.cell(row=i + 1, column=column + 1).border = well_data.thin_border
                    if column == 1 or column == 11:
                        ws2.cell(row=i + 1, column=column + 1).alignment = Alignment(wrap_text=True,
                                                                                     horizontal='center',
                                                                                     vertical='center')
                        ws2.cell(row=i + 1, column=column + 1).font = Font(name='Arial', size=13, bold=False)
                    else:
                        ws2.cell(row=i + 1, column=column + 1).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                                     vertical='center')
                        ws2.cell(row=i + 1, column=column + 1).font = Font(name='Arial', size=13, bold=False)
                        if 'примечание' in str(ws2.cell(row=i + 1, column=column + 1).value).lower() or \
                                'внимание' in str(ws2.cell(row=i + 1, column=column + 1).value).lower() or \
                                'мероприятия' in str(ws2.cell(row=i + 1, column=column + 1).value).lower() or \
                                'порядок работ' in str(ws2.cell(row=i + 1, column=column + 1).value).lower() or \
                                'По доп.согласованию с Заказчиком' in str(
                            ws2.cell(row=i + 1, column=column + 1).value).lower():
                            # print('есть жирный')
                            ws2.cell(row=i + 1, column=column + 1).font = Font(name='Arial', size=13, bold=True)

                if len(work_list[i][1]) > 5:
                    ws2.merge_cells(start_column=2, start_row=i + 1, end_column=12, end_row=i + 1)
                    ws2.cell(row=i + 1, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
                    ws2.cell(row=i + 1, column=2).fill = PatternFill(start_color='C5D9F1', end_color='C5D9F1',
                                                                     fill_type='solid')
                    ws2.cell(row=i + 1, column=2).font = Font(name='Arial', size=13, bold=True)
                elif i <= 32:
                    ws2.merge_cells(start_column=3, start_row=i + 1, end_column=11, end_row=i + 1)
                    ws2.cell(row=i + 1, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                        vertical='center')
                    ws2.cell(row=i + 1, column=11).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')
                else:
                    ws2.merge_cells(start_column=3, start_row=i + 1, end_column=10, end_row=i + 1)
                    ws2.cell(row=i + 1, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                        vertical='center')
                    ws2.cell(row=i + 1, column=11).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')

            for col in range(13):
                ws2.column_dimensions[get_column_letter(col + 1)].width = colWidth[col]
            ws2.column_dimensions[get_column_letter(11)].width = 30
            ws2.print_area = f'B1:L{self.table_widget.rowCount() + 45}'
            ws2.page_setup.fitToPage = True
            ws2.page_setup.fitToHeight = False
            ws2.page_setup.fitToWidth = True
            ws2.print_options.horizontalCentered = True
            # зададим размер листа
            ws2.page_setup.paperSize = ws2.PAPERSIZE_A4
            # содержимое по ширине страницы
            ws2.sheet_properties.pageSetUpPr.fitToPage = True
            ws2.page_setup.fitToHeight = False

        for row_ind, row in enumerate(ws2.iter_rows(values_only=True)):
            for col, value in enumerate(row):
                if 'Ойл' in well_data.contractor:
                    if 'А.Р. Хасаншин' in str(value):
                        coordinate = f'{get_column_letter(col + 1)}{row_ind - 1}'
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/Хасаншин.png', coordinate)
                    elif 'Д.Д. Шамигулов' in str(value):
                        coordinate = f'{get_column_letter(col + 1)}{row_ind - 2}'
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/Шамигулов.png', coordinate)
                    elif 'Зуфаров' in str(value):
                        coordinate = f'{get_column_letter(col - 2)}{row_ind}'
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/Зуфаров.png', coordinate)
                    elif 'М.К.Алиев' in str(value):
                        coordinate = f'{get_column_letter(col - 1)}{row_ind - 2}'
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/Алиев махир.png', coordinate)
                    elif 'З.К. Алиев' in str(value):
                        coordinate = f'{get_column_letter(col - 1)}{row_ind - 2}'
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/Алиев Заур.png', coordinate)
                        break

    def work_with_data_gnkt(self):
        if self.data_gnkt is None:

            self.data_gnkt = GnktOsvWindow2(self)
            self.data_gnkt.setWindowTitle("Данные по ГНКТ")
            self.data_gnkt.setGeometry(200, 400, 100, 400)
            self.data_gnkt.show()
            self.pause_app()
            well_data.pause = True

            if well_data.work_plan in ['gnkt_after_grp', 'gnkt_opz', 'gnkt_bopz']:
                self.work_schema = self.data_gnkt.schema_well(self.data_gnkt.current_bottom_edit,
                                                              self.data_gnkt.fluid_edit,
                                                              self.data_gnkt.gnkt_number_combo,
                                                              self.data_gnkt.lenght_gnkt_edit,
                                                              self.data_gnkt.iznos_gnkt_edit,
                                                              self.data_gnkt.pvo_number,
                                                              self.data_gnkt.diametr_length,
                                                              self.data_gnkt.pipe_mileage_edit)

                self.copy_pvr(self.ws_schema, self.work_schema)
        else:
            self.data_gnkt.close()
            self.data_gnkt = None

    def update_opz_data(self, current_widget):

        self.roof_plast = round(float(current_widget.roof_edit.text().replace(',', '.')), 1)
        self.sole_plast = round(float(current_widget.sole_edit.text().replace(',', '.')), 1)

        self.acid_edit = current_widget.acid_edit.currentText()

        self.acid_volume_edit = float(current_widget.acid_volume_edit.text().replace(',', '.'))
        self.acid_proc_edit = int(current_widget.acid_proc_edit.text().replace(',', '.'))
        self.pressure_edit = int(current_widget.pressure_edit.text())
        self.plast_combo = str(current_widget.plast_combo.combo_box.currentText())

    def add_work(self):
        self.current_widget = self.tabWidget.currentWidget()
        self.gnkt_number_combo = self.current_widget.gnkt_number_combo.currentText()
        self.lenght_gnkt_edit = self.current_widget.lenght_gnkt_edit.text()
        self.iznos_gnkt_edit = self.current_widget.iznos_gnkt_edit.text().replace(',', '.')
        self.pipe_mileage_edit = self.current_widget.pipe_mileage_edit.text()
        self.distance_pntzh = self.current_widget.distance_pntzh_line.text()
        self.pipe_fatigue = 0

        self.current_bottom_edit = self.current_widget.current_bottom_edit.text()
        if self.current_bottom_edit == '':
            QMessageBox.warning(self, 'Некорректные данные', f'не указан текущий забоя')
            return
        else:
            self.current_bottom_edit = float(self.current_bottom_edit.replace(',', '.'))
            if self.current_bottom_edit > float(well_data.bottomhole_drill._value):
                QMessageBox.warning(self, 'Некорректные данные',
                                    f'Текущий забой ниже пробуренного забоя {well_data.bottomhole_drill._value}')
                return

        self.fluid_edit = self.current_widget.fluid_edit.text()

        if well_data.work_plan in ['gnkt_after_grp', 'gnkt_frez']:

            self.acids_work_combo = self.current_widget.acids_work_combo.currentText()
            if self.acids_work_combo == '':
                QMessageBox.critical(self, "Ошибка", "Нужно выбрать необходимость фрезерования")
                return

            if self.acids_work_combo == 'Да':
                self.update_opz_data(self.current_widget)
                if self.roof_plast in ['', None, 0] or self.sole_plast in ['', None, 0]:
                    QMessageBox.critical(self, "Ошибка", "Не введены данные по кровле и ли подошве обработки")
                    return
            if well_data.work_plan == 'gnkt_frez':
                self.need_frez_port = self.current_widget.need_frez_port_combo.currentText()
                if self.need_frez_port == '':
                    QMessageBox.critical(self, "Ошибка", "Нужно выбрать необходимость фрезерования")
                    return
            elif well_data.work_plan == 'gnkt_after_grp':
                self.osvoenie_combo_need = self.current_widget.osvoenie_combo.currentText()
                if self.osvoenie_combo_need == '':
                    QMessageBox.critical(self, "Ошибка", "Нужно выбрать необходимость освоения")
                    return

        self.pvo_number = self.current_widget.pvo_number_edit.text()

        self.previous_well_combo = self.current_widget.previous_well_combo.currentText()

        self.diametr_length = 38

        if '' in [self.gnkt_number_combo, self.lenght_gnkt_edit, self.iznos_gnkt_edit, self.fluid_edit,
                  self.pvo_number]:
            QMessageBox.warning(self, 'Некорректные данные', f'Не все данные заполнены')
            return
        else:
            well_data.gnkt_number_combo = self.gnkt_number_combo
            well_data.lenght_gnkt_edit = float(self.lenght_gnkt_edit)
            well_data.iznos_gnkt_edit = float(self.iznos_gnkt_edit)
            well_data.fluid_edit = self.fluid_edit
            well_data.pvo_number = self.pvo_number

        fluid_question = QMessageBox.question(self, 'Удельный вес',
                                              f'Работы необходимо производить на тех воде {self.fluid_edit}г/см3?')
        if fluid_question == QMessageBox.StandardButton.No:
            return

        self.well_volume_ek, self.well_volume_dp = self.check_volume_well()

        well_data.pause = False
        self.close()
        # return work_list

    def select_text_acid(self, plast_combo, roof, sole, acid_edit, acid_proc_edit, acid_volume_edit):

        if acid_edit == 'HCl':
            acid_24 = round(acid_volume_edit * acid_proc_edit / 24 * 1.118, 1)
            acid_sel = f'Произвести  солянокислотную обработку {plast_combo} в объеме {acid_volume_edit}м3 ' \
                       f' ({acid_edit} - {acid_proc_edit} %) силами/' \
                       f' Крезол НС с протяжкой БДТ вдоль интервалов перфорации {roof}-{sole}м ' \
                       f'(снизу вверх) в ' \
                       f'присутствии представителя заказчика с составлением акта, не превышая давления' \
                       f' закачки не более Р={well_data.max_admissible_pressure._value}атм.\n' \
                       f' (для приготовления соляной кислоты в объеме {acid_volume_edit}м3 - ' \
                       f'{acid_proc_edit}% необходимо замешать {acid_24}т HCL 24% и пресной воды ' \
                       f'{round(acid_volume_edit - acid_24, 1)}м3)'
            acid_sel_short = f'СКО пласта {plast_combo} {roof}-{sole} в объеме  {acid_volume_edit}м3  ' \
                             f'({acid_edit} - {acid_proc_edit} %)'
        elif acid_edit == 'ВТ':
            acid_sel = f'Произвести кислотную обработку пласта f{roof}-{sole}м {acid_edit} силами Крезол ' \
                       f'НС с протяжкой БДТ вдоль интервалов перфорации {roof}-{sole}м (снизу вверх) в присутствии ' \
                       f'представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более ' \
                       f'Р = {well_data.max_admissible_pressure._value}атм.'
            acid_sel_short = f'{acid_edit} пласта {plast_combo}  в объеме ' \
                             f'{acid_volume_edit}м3  ({acid_edit} - {acid_proc_edit} %)'
        elif acid_edit == 'HF':
            acid_sel = f'Произвести глинокислотную обработку пласта {plast_combo} в объеме ' \
                       f'{acid_volume_edit}м3 ' \
                       f'(концентрация в смеси HF 3% / HCl 13%) силами Крезол ' \
                       f'НС с протяжкой БДТ вдоль интервалов перфорации {roof}-{sole}м (снизу вверх) в' \
                       f' присутствии представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более ' \
                       f'Р={well_data.max_admissible_pressure._value}атм.'
            acid_sel_short = f'ГКО пласта {plast_combo}  в объеме  {acid_volume_edit}м3'
        elif acid_edit == 'Лимонная кислота':
            acid_sel = f'Произвести лимонной кислотой пласта {plast_combo} в объеме ' \
                       f'{acid_volume_edit}м3 ' \
                       f'с протяжкой БДТ вдоль интервалов перфорации {roof}-{sole}м (снизу вверх) в присутствии' \
                       f' представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более ' \
                       f'Р={well_data.max_admissible_pressure._value}атм.'
            acid_sel_short = f'КО лимонной кислотой пласта {plast_combo} в объеме {acid_volume_edit}м3'

        return acid_sel, acid_sel_short

    def work_opz_gnkt(self, acid_info):

        self.volume_gntk = round(float(well_data.lenght_gnkt_edit) * 0.74 / 1000, 1)

        depth_fond_paker_do = sum(map(int, list(well_data.dict_nkt.values())))
        if well_data.depth_fond_paker_do["do"] == 0:
            self.depth_fond_paker_do = sum(list(well_data.dict_nkt.values()))
            # print(depth_fond_paker_do)
            if self.depth_fond_paker_do >= well_data.current_bottom:
                depth_fond_paker_do, ok = QInputDialog.getDouble(self, 'глубина НКТ',
                                                                 'Введите Глубины башмака НКТ', 500,
                                                                 0, well_data.current_bottom)
        else:
            self.depth_fond_paker_do = well_data.depth_fond_paker_do["do"]

        opz = []
        volume_sko = 0
        for plast_combo,skv_como, roof, sole, acid_edit, acid_proc_edit, acid_volume_edit in acid_info:
            acid_sel, acid_sel_short = self.select_text_acid(plast_combo, roof, sole, acid_edit, acid_proc_edit,
                                                             acid_volume_edit)
            volume_sko += acid_volume_edit

            opz.extend([[f'Установить КНК до глубины {sole}м',
                        17, f'Установить КНК до глубины {sole}м',
                        None, None, None, None, None, None, None,
                        'Мастер ГНКТ, состав бригады', 0.2],
                        [acid_sel_short,
                         17, acid_sel,
                         None, None, None, None, None, None, None,
                         'Мастер ГНКТ, состав бригады, подрядчик по ОПЗ', 2]]
                       )
        opz.insert(0,             [None,
             f'КИСЛОТНАЯ ОБРАБОТКА в объеме {volume_sko}м3 {acid_edit} {acid_proc_edit}% ',
             None, None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', None])

        work_list = [[None,
                      18,
                      f'ПРИМЕЧАНИЕ:\n '
                      f'Закачку первого объема {self.volume_gntk}м3 кислоты производить при открытом малом '
                      f'затрубном пространстве на '
                      f'циркуляции. Закачку оставшейся '
                      f'кислоты в объеме {round(volume_sko - self.volume_gntk, 1)}м3 производить '
                      f'при закрытом малом затрубном '
                      f'пространстве. Составить Акт.',
                      None, None, None, None, None, None, None,
                      'Мастер ГНКТ, состав бригады', 2.88],
                     [None, 19, f'Продавить кислоту в пласт мин.водой уд.веса {well_data.fluid_work} в объёме '
                                f'{round(self.volume_gntk + 1.5, 1)}м3 при '
                                f'давлении не более '
                                f'{well_data.max_admissible_pressure._value}атм. Составить Акт',
                      None, None, None, None, None, None, None,
                      'Мастер ГНКТ, состав бригады', 1.11],
                     [None, 20,
                      f'Приподнять БДТ на {int(self.depth_fond_paker_do) - 20}м. Стоянка на реакции 2 часа. В СЛУЧАЕ'
                      f' ОТСУТСТВИЯ ДАВЛЕНИЯ '
                      f'ПРОДАВКИ ПРИ СКО, РАБОТЫ ПРОИЗВОДИМ БЕЗ РЕАГИРОВАНИЯ.СОСТАВИТЬ АКТ)',
                      None, None, None, None, None, None, None,
                      'Мастер ГНКТ, состав бригады', 3.06],
                     ['разрядку скважины для извлечения продуктов',
                      21,
                      'Произвести разрядку скважины для извлечения продуктов реакции кислоты в объёме не менее объёма '
                      'закаченной кислоты + объём малого затрубного пространства (из расчета 1,88л на 1 м пространства между '
                      '73мм колонной НКТ и БДТ;'
                      ' 0,46л между 60мм НКТ и БДТ; 3,38л между 89мм НКТ и БДТ) + 3м3. Разрядку производить до чистой'
                      ' промывочной '
                      'жидкости (без признаков продуктов реакции кислоты), но не более 2 часов. Зафиксировать '
                      'избыточное давление '
                      'на устье скважины, объём и описание скважинной жидкости на выходе с отражением их в акте,'
                      ' суточном рапорте '
                      'работы бригад. Составить Акт.',
                      None, None, None, None, None, None, None,
                      'Мастер ГНКТ, состав бригады', 1],
                     ['Допустить БДТ до забоя. Промыть скважину ',
                      16,
                      f'Допустить БДТ до забоя. Промыть скважину  мин.водой уд.веса {well_data.fluid_work}  с составлением '
                      f'соответствующего акта. При отсутствии циркуляции дальнейшие промывки исключить. Определить '
                      f'приемистость пласта в трубное пространство при давлении не более '
                      f'{well_data.max_admissible_pressure._value}атм'
                      f'  (перед определением приемистости произвести закачку тех.воды не менее 6м3 или при установившемся '
                      f'давлении закачки, но не более 1 часа). Установить БДТ на гл.{well_data.current_bottom}м.',
                      None, None, None, None, None, None, None,
                      'Мастер ГНКТ, состав бригады, представитель Заказчика', 1.33],
                     ]
        opz.extend(work_list)
        return opz

    @staticmethod
    def check_volume_well():
        if well_data.column_additional:
            well_volume_ek = well_volume(None, well_data.head_column_additional._value)
        else:
            well_volume_ek = well_volume(None, well_data.current_bottom)
        if abs(float(well_data.well_volume_in_PZ[0]) - well_volume_ek) > 0.2:
            QMessageBox.warning(None, 'Некорректный объем скважины',
                                f'Объем скважины указанный в ПЗ -{well_data.well_volume_in_PZ}м3 не совпадает '
                                f'с расчетным {well_volume_ek}м3')
            well_volume_ek, _ = QInputDialog.getDouble(None,
                                                       "корректный объем",
                                                       'Введите корректный объем', well_data.well_volume_in_PZ[0], 1,
                                                       80, 1)
            well_volume_dp = well_volume(None, well_data.current_bottom) - well_volume_ek
        else:
            well_volume_dp = well_volume(None, well_data.current_bottom) - well_volume_ek
        return well_volume_ek, well_volume_dp

    def schema_well(self, current_bottom_edit, fluid_edit, gnkt_number_combo,
                    gnkt_lenght, iznos_gnkt_edit, pvo_number, diametr_length, pipe_mileage_edit):
        self.gnkt = self.tabWidget.currentWidget()
        for plast_ind in well_data.plast_work:
            try:
                self.plast_work = plast_ind
                plast_work = self.plast_work

                self.pressuar = list(well_data.dict_perforation[plast_work]["давление"])[0]

                zamer = list(well_data.dict_perforation[plast_work]['замер'])[0]
                vertikal = min(map(float, list(well_data.dict_perforation[plast_work]["вертикаль"])))
                break
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка прочтения данных ПВР {e}')

        koef_anomal = round(float(self.pressuar) * 101325 / (float(vertikal) * 9.81 * 1000), 1)

        nkt_str = ''
        lenght_str = '0-'
        vn_str = ''
        nkt_widht_str = ''
        sorted_dict = dict(sorted(well_data.dict_nkt.items(), reverse=True))
        len_a = 0
        volume_vn_str = ''
        volume_str = ''
        nkt_lenght = 0
        for nkt_in, lenght in sorted_dict.items():
            nkt_lenght += lenght
            if '60' in str(nkt_in):
                nkt_in = 60
                nkt_str += f'{nkt_in}\n'
                nkt_widht = 5
                nkt_widht_str += f'{nkt_widht}\n'
                vn_str += f'{nkt_in - 2 * nkt_widht}\n'
                volume_vn = round((nkt_in - 2 * nkt_widht) ** 2 * 3.14 / 4 / 1000, 1)
                volume_vn_str += f'{volume_vn}\n'
                volume = round((volume_vn * lenght) / 1000, 1)
                volume_str += f'{volume}\n'

            elif '73' in str(nkt_in):
                nkt_in = 73
                nkt_str += f'{nkt_in}\n'
                nkt_widht = 5.5
                nkt_widht_str += f'{nkt_widht}\n'
                vn_str += f'{nkt_in - 2 * nkt_widht}\n'
                volume_vn = round((nkt_in - 2 * nkt_widht) ** 2 * 3.14 / 4 / 1000, 1)
                volume_vn_str += f'{volume_vn}\n'
                volume = round((volume_vn * lenght) / 1000, 1)
                volume_str += f'{volume}\n'
            elif '89' in str(nkt_in):
                nkt_in = 89
                nkt_str += f'{nkt_in}\n'
                nkt_widht = 7.34
                nkt_widht_str += f'{nkt_widht}\n'
                vn_str += f'{nkt_in - 2 * nkt_widht}\n'
                volume_vn = round((nkt_in - 2 * nkt_widht) ** 2 * 3.14 / 4 / 1000, 1)
                volume_vn_str += f'{volume_vn}\n'
                volume = round((volume_vn * lenght) / 1000, 1)
                volume_str += f'{volume}\n'

            lenght_str += f'{lenght + len_a}\n{lenght}-'
            len_a += lenght

        nkt_widht_str = nkt_widht_str[:-1]
        lenght_str = lenght_str.split('\n')
        lenght_str = lenght_str[:-1]
        volume_str = volume_str.split('\n')[:-1]
        volume_str = '\n'.join(volume_str)
        volume_vn_str = volume_vn_str.split('\n')[:-1]
        volume_vn_str = '\n'.join(volume_vn_str)
        nkt_str = nkt_str[:-1]
        vn_str = vn_str[:-1]

        lenght_nkt = '\n'.join(lenght_str)

        volume_vn_gnkt = round(30.2 ** 2 * 3.14 / (4 * 1000), 2)

        volume_gnkt = round(float(gnkt_lenght) * volume_vn_gnkt / 1000, 1)

        volume_pm_ek = round(
            3.14 * (well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value) ** 2 / 4 / 1000, 2)
        volume_pm_dp = round(3.14 * (well_data.column_additional_diametr._value - 2 *
                                     well_data.column_additional_wall_thickness._value) ** 2 / 4 / 1000, 2)

        if well_data.column_additional:
            column_data_add_diam = well_data.column_additional_diametr._value
            column_data_add_wall_thickness = well_data.column_additional_wall_thickness._value

            column_data_add_vn_volume = round(
                well_data.column_additional_diametr._value - 2 * well_data.column_additional_wall_thickness._value, 1)
            column_add_head = well_data.head_column_additional._value
            column_add_shoe = well_data.shoe_column_additional._value

        else:
            column_data_add_diam = ''
            column_data_add_wall_thickness = ''

            column_data_add_vn_volume = ''
            column_add_head = ''
            column_add_shoe = ''
        if well_data.curator == 'ОР':
            expected_title = 'Ожидаемый приемистость скважины'
            Qoil = f'{well_data.expected_Q}м3/сут'
            Qwater = f'{well_data.expected_P}атм'
            proc_water = ''
        else:
            expected_title = 'Ожидаемый дебит скважины'
            Qoil = f'{well_data.Qoil}т/сут'
            Qwater = f'{well_data.Qwater}м3/сут'
            proc_water = f'{well_data.proc_water}%'

        nkt = list(well_data.dict_nkt.keys())
        if len(nkt) != 0:
            nkt = nkt[0]

        wellhead_fittings = well_data.wellhead_fittings
        if well_data.work_plan == 'gnkt_after_grp':

            if 'грп' in str(well_data.wellhead_fittings).lower():
                wellhead_fittings = well_data.wellhead_fittings
            else:
                wellhead_fittings = f'АУШГН-{well_data.column_diametr._value}/' \
                                    f'АУГРП {well_data.column_diametr._value}*14'

        elif well_data.work_plan == 'gnkt_bopz':

            list_gnkt_bopz = [
                None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None,
                f'{plast_work}\n{well_data.dict_perforation[plast_work]["кровля"]}-{well_data.dict_perforation[plast_work]["подошва"]}',
                None,
                None, None, None, f'Тек. забой: \n{well_data.current_bottom}м ', None]
        lenght_paker = 2
        voronka = well_data.depth_fond_paker_do["do"]
        if well_data.curator == 'ОР' and well_data.region == 'ТГМ':
            lenght_paker = round(
                float(well_data.depth_fond_paker2_do["do"]) - float(well_data.depth_fond_paker_do["do"]), 1)
            voronka = round(nkt_lenght + lenght_paker, 1)
        schema_well_list = [
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, 'СХЕМА СКВАЖИНЫ', None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Данные о размерности труб', None,
             None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Тип ПВО', None, None,
             f'4-х секционный превентор БП 80-70.00.00.000 (700атм) К2 № {pvo_number}', None, None, None, None, None,
             None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Тип ФА', None, None,
             wellhead_fittings, None, None, None,
             None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Тип КГ', None, None,
             well_data.column_head_m, None,
             None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, f'ЭК {well_data.column_diametr._value}мм', None,
             None,
             'Стол ротора', None, f'{well_data.stol_rotora._value}м',
             'Øнаруж мм', 'толщ, мм', 'Øвнут, мм', 'Интервал спуска, м', None, 'ВПЦ.\nДлина', 'Объем', None],
            [None, None, None, None, None, None, None, None, None, f'0-{well_data.shoe_column._value}м', None, None,
             'Ø канавки', None, f'{well_data.groove_diameter}', None, None,
             None, None, None, None, 'л/п.м.', 'м3'],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Шахтное направление', None, None,
             "", None, None, "", "", '', None, None],
            [None, None, None, None, None, None, None, None, None, f'НКТ {nkt_str}мм', None, None, 'Направление', None,
             None,
             f'{well_data.column_direction_diametr._value}', well_data.column_direction_wall_thickness._value,
             round(well_data.column_direction_diametr._value - 2 * well_data.column_direction_wall_thickness._value, 1),
             f'0-', well_data.column_direction_lenght._value,
             f'{well_data.level_cement_direction._value}-{well_data.column_direction_lenght._value}', None,
             None],
            [None, None, None, None, None, None, None, None, None, f'{lenght_nkt}м', None, None, 'Кондуктор',
             None, None, well_data.column_conductor_diametr._value, well_data.column_conductor_wall_thickness._value,
             f'{round(well_data.column_conductor_diametr._value - 2 * well_data.column_conductor_wall_thickness._value)}',
             f'0-', well_data.column_conductor_lenght._value,
             f'{well_data.level_cement_conductor._value}-{well_data.column_conductor_lenght._value}', None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Экспл. колонна', None, None,
             f'{well_data.column_diametr._value}', f'{well_data.column_wall_thickness._value}',
             f'{round(float(well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value), 1)}',
             f'0-', well_data.shoe_column._value, f'0-{well_data.level_cement_column._value}', volume_pm_ek,
             self.well_volume_ek],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, "", ""],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, "", ""],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, "", ""],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Тех.колонна', None, None,
             column_data_add_diam,
             column_data_add_wall_thickness, column_data_add_vn_volume, column_add_head, column_add_shoe, None,
             volume_pm_dp, self.well_volume_dp],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'колонна НКТ', None, None, nkt_str,
             nkt_widht_str, vn_str, lenght_nkt, None, None, volume_vn_str, volume_str],
            [None, None, None, None, None, None, None, None, None, None, None, None, f'{well_data.paker_do["do"]}',
             None, None, None, None,
             50, well_data.depth_fond_paker_do["do"], round(well_data.depth_fond_paker_do["do"] + lenght_paker, 1),
             lenght_paker, None, None],
            [None, None, None, None, None, None, None, None, None, 'пакер', None, None, 'без патрубка', None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, f'на гл {well_data.depth_fond_paker_do["do"]}м',
             None, None,
             'воронка', None, None, nkt, None,
             None, voronka, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Данные о перфорации', None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, 'воронка', None, None, 'Пласт\nгоризонт', None,
             'Глубина пласта по вертикали', None, 'Интервал перфорации', None, None, None, 'вскрытия/\nотключения',
             'Рпл. атм', None],
            [None, None, None, None, None, None, None, None, None, f'на гл.{voronka}м', None, None, None, None, None,
             None, 'от', None, 'до', None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Данные о забое', None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Тек. забой по ПЗ ', None, None,
             None, None, None, None, None, None, well_data.bottom, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'необходимый текущий забой ', None, None, None, None, None, None, None, None, current_bottom_edit, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Искусственный забой  ', None,
             None, None, None, None, None, None, None, well_data.bottomhole_artificial._value, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Дополнительная информация', None,
             None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Категория скважины', None, None,
             None, None, well_data.category_pressuar, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Содержание H2S, мг/л', None, None,
             None,
             None, 'отсут' if well_data.h2s_mg[0] is None else well_data.h2s_mg[0], None, None, None, None, None],
            [None, None, None, None, None, None, None, None,
             None, None, None, None, 'Газовый фактор', None, None, None,
             None, well_data.gaz_f_pr[0], None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Коэффициент аномальности', None,
             None, None, None, koef_anomal, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Плотность жидкость глушения',
             None, None, None, None, fluid_edit, None, 'в объеме', None, self.well_volume_ek, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, expected_title, None,
             None, None, None, Qoil, None, Qwater, None, proc_water, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Максимальный угол наклона', None,
             None, None, None, well_data.max_angle._value, None, 'на глубине', None, well_data.max_angle_H._value,
             None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Интервалы темпа набора кривизны более 1,5°  на 10 м', None,
             None, None, None, well_data.interval_temp._value, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Дата начало / окончания бурения',
             None, None, None, None, self.date_dmy(well_data.date_drilling_run), None,
             self.date_dmy(well_data.date_drilling_cancel),
             None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Дата ввода в эксплуатацию', None,
             None, None, None, f'{well_data.сommissioning_date}', None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Р в межколонном пространстве',
             None, None, None, None, well_data.pressuar_mkp._value, None, ' ', None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Первоначальное Р опр-ки ЭК', None,
             None, None, None, well_data.first_pressure._value, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Результат предыдущей опрес-и ЭК',
             None, None, None, None, well_data.rezult_pressuar._value, None, '', None, 'гермет.', None],
            [None, None, None, None, None, None, None, None, 'Тек.забой' if well_data.work_plan != 'gnkt_bopz' else '',
             None, None, None,
             'Макс.допустимое Р опр-ки ЭК', None, None, None, None, well_data.max_admissible_pressure._value,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None,
             current_bottom_edit if well_data.work_plan != 'gnkt_bopz' else '', None, None, None,
             'Макс. ожидаемое Р на устье ',
             None, None, None, None, well_data.max_expected_pressure._value, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, f'флот {gnkt_number_combo}',
             None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, 'длина трубы', 'Øнаруж мм', 'толщ, мм',
             'Øвнут, мм', 'Объем', None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'л/п.м.', None,
             'м3', None, '%', None, 'м', None, None],
            [None, None, None, None, None, None, None, None, None, None, None, gnkt_lenght,
             diametr_length, 3.68, '=M67-2*N67',
             '=ROUND(O67*O67*3.14/4/1000,2)', None, '=ROUND(L67*P67/1000, 1)', None, iznos_gnkt_edit, None,
             pipe_mileage_edit, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, 'объем наземной линии, м3', None,
             'объем до границы перфорации, м3', None, 'Объем продавки, м3 ', None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, 1, None, '=L67*P67/1000', None,
             '=L70+N70', None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, 'Вид и категория ремонта, его шифр',
             None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None,
             f'{well_data.type_kr}', None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None,
             None, f'{well_data.bur_rastvor}', None, None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None],
        ]

        if well_data.work_plan == 'gnkt_bopz':
            schema_well_list.append(list_gnkt_bopz)
        if well_data.paker_do['do'] == 0:
            schema_well_list[21] = [None, None, None, None, None, None, None, None, None, None,
                                    None, None,
                                    'воронка', None, None, nkt, None,
                                    None, well_data.depth_fond_paker_do["do"], None, None, None, None]
            schema_well_list[20] = [None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                                    None,
                                    None, None, None, None, None, None, None, None]
            schema_well_list[19] = [None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                                    None,
                                    None, None, None, None, None, None, None, None]

        pvr_list = []
        well_data.img_pvr_list = []
        for plast in sorted(well_data.plast_all, key=lambda x: self.get_start_depth(
                well_data.dict_perforation[x]['интервал'][0])):
            count_interval = 0
            for interval in well_data.dict_perforation[plast]['интервал']:

                if well_data.dict_perforation[plast]['отключение']:
                    izol = 'Изолирован'
                else:
                    count_interval += 1
                    well_data.img_pvr_list = [(plast, well_data.dict_perforation[plast]['интервал'])]
                    izol = 'рабочий'
                if well_data.paker_do['do'] != 0:
                    if well_data.dict_perforation[plast]['кровля'] < well_data.depth_fond_paker_do['do']:
                        izol = 'над пакером'
                try:
                    pressuar = well_data.dict_perforation[plast]['давление'][0]
                    zamer = well_data.dict_perforation[plast]['замер'][0]
                except:
                    pressuar = None
                    zamer = None
                pvr_list.append(
                    [None, None, None, None, None, None, None, None, None, None, None, None, plast, None, vertikal,
                     None, interval[0],
                     None, interval[1], None, izol, pressuar,
                     zamer, None], )
            well_data.dict_perforation[plast]['счет_объединение'] = count_interval

        for index, pvr in enumerate(pvr_list):
            schema_well_list[26 + index] = pvr

        well_data.current_bottom = round(float(current_bottom_edit), 1)

        return schema_well_list



    def create_title_list(self, ws2):

        # print(f'цднг {well_data.cdng._value}')
        well_data.region = block_name.region_select(well_data.cdng._value)

        self.region = well_data.region

        title_list = [
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, 'ЗАКАЗЧИК:', None, None, None, None, None, None, None, None, None, None],
            [None, 'ООО «Башнефть-Добыча»', None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, 'ПЛАН РАБОТ НА СКВАЖИНЕ С ПОМОЩЬЮ УСТАНОВКИ С ГИБКОЙ ТРУБОЙ', None, None, None,
             None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, '№ скважины:', f'{well_data.well_number._value}', 'куст:', None, 'Месторождение:', None, None,
             well_data.well_oilfield._value, None, None],
            [None, None, 'инв. №:', well_data.inv_number._value, None, None, None, None, 'Площадь: ',
             well_data.well_area._value,
             None,
             1],
            [None, None, None, None, None, None, None, 'цех:', f'{well_data.cdng._value}', None, None, None]]

        razdel = razdel_1(self, well_data.region, well_data.contractor)

        for row in razdel:  # Добавлением работ
            title_list.append(row)

        for row in [
            [None, None, None, None, None, "дата", datetime.now().strftime('%d.%m.%Y'), None, None, None, None]]:
            title_list.insert(-1, row)
        # print(title_list)
        index_insert = 11
        ws2.cell(row=1, column=2).alignment = Alignment(wrap_text=False, horizontal='left',
                                                        vertical='center')
        ws2.cell(row=1, column=4).alignment = Alignment(wrap_text=False, horizontal='left',
                                                        vertical='center')
        # ws2.column_dimensions[get_column_letter(1)].width = 15
        # ws2.column_dimensions[get_column_letter(2)].width = 20
        # ws2.column_dimensions[get_column_letter(3)].width = 20
        a = None
        for row in range(len(title_list)):  # Добавлением работ
            if row not in range(8, 13):
                ws2.row_dimensions[row].height = 35
            for col in range(1, 12):
                ws2.column_dimensions[get_column_letter(col)].width = 15
                cell = ws2.cell(row=row + index_insert, column=col)
                # print(f' Х {title_list[i ][col - 1]}')
                if title_list[row - 1][col - 1] != None:
                    ws2.cell(row=row + index_insert, column=col).value = str(title_list[row - 1][col - 1])
                ws2.cell(row=row + index_insert, column=col).font = Font(name='Arial', size=11, bold=False)
                ws2.cell(row=row + index_insert, column=col).alignment = Alignment(wrap_text=False, horizontal='left',
                                                                                   vertical='center')
                if 'ПЛАН РАБОТ' in str(title_list[row - 1][col - 1]):
                    ws2.merge_cells(start_row=row + index_insert, start_column=2, end_row=row + index_insert,
                                    end_column=11)
                    ws2.merge_cells(start_row=row - 4 + index_insert, start_column=2, end_row=row - 4 + index_insert,
                                    end_column=4)
                    ws2.cell(row=row + index_insert, column=col).font = Font(name='Arial', size=14, bold=True)
                    ws2.cell(row=row + index_insert, column=col).alignment = Alignment(wrap_text=False,
                                                                                       horizontal='center',
                                                                                       vertical='center')
                if 'СОГЛАСОВАНО:' in str(title_list[row - 1][col - 1]):
                    a = row + index_insert

            # for row in range(len(title_list)):  # Добавлением работ
            if a:
                if a > row:
                    # print(f'сссооссоссо {row + index_insert}')
                    ws2.merge_cells(start_row=row + index_insert, start_column=2, end_row=row + index_insert,
                                    end_column=6)
                    ws2.merge_cells(start_row=row + index_insert, start_column=8, end_row=row + index_insert,
                                    end_column=11)

        ws2.print_area = f'B1:K{44}'
        ws2.page_setup.fitToPage = True
        ws2.page_setup.fitToHeight = False
        ws2.page_setup.fitToWidth = True
        ws2.print_options.horizontalCentered = True
        # зададим размер листа
        ws2.page_setup.paperSize = ws2.PAPERSIZE_A4

    def date_dmy(self, date_str):
        print(date_str, type(date_str))
        if '-' in str(date_str):
            return date_str
        elif type(date_str) is datetime:
            date_obj = datetime.strftime('%d.%m.%Y')
        else:
            date_obj = date_str

        return date_obj

    # Функция для получения глубины начала интервала
    def get_start_depth(self, interval):
        return interval[0]

    def calc_fluid(self):

        fluid_list = []
        try:

            fluid_p = 0.83
            for plast in well_data.plast_work:
                if float(list(well_data.dict_perforation[plast]['рабочая жидкость'])[0]) > fluid_p:
                    fluid_p = list(well_data.dict_perforation[plast]['рабочая жидкость'])[0]
            fluid_list.append(fluid_p)

            fluid_work_insert, ok = QInputDialog.getDouble(self, 'Рабочая жидкость',
                                                           'Введите расчетный удельный вес жидкости глушения в '
                                                           'конце жидкости',
                                                           max(fluid_list), 0.87, 2, 2)
        except:
            fluid_work_insert, ok = QInputDialog.getDouble(self, 'Рабочая жидкость',
                                                           'Введите удельный вес рабочей жидкости',
                                                           0, 0.87, 2, 2)
        return fluid_work_insert


class GnktOsvWindow2(GnktModel):
    def __init__(self, parent=None):
        super().__init__()


if __name__ == '__main__':
    app = QApplication([])
    window = GnktOsvWindow2()
    window.show()
    app.exec_()
