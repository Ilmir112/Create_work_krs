import logging

from PyQt5.QtGui import QDoubleValidator, QIntValidator

import data_list

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, \
    QTableWidget, QHeaderView, QPushButton, QTableWidgetItem, QApplication, QMainWindow

from main import MyMainWindow
from work_py.alone_oreration import well_volume
from work_py.parent_work import TabWidgetUnion, WindowUnion, TabPageUnion
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm, well_volume_norm
from work_py.rir import RirWindow
from  work_py.opressovka import TabPageSo


class TabPageSoPakerIzv(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(0, 80000)

        self.pero_diameter_label = QLabel("Диаметр пакера", self)
        self.pero_diameter_line = QLineEdit(self)

        self.paker_type_label = QLabel("Тип извлекаемого пакер", self)
        self.paker_type_combo = QComboBox(self)
        raid_type_list = ['РКИ']
        self.paker_type_combo.addItems(raid_type_list)

        self.nkt_select_label = QLabel("компоновка НКТ", self)
        self.nkt_select_combo = QComboBox(self)
        self.nkt_select_combo.addItems(['пакер в ЭК', 'пакер в ДП'])

        if self.data_well.column_additional is False or (self.data_well.column_additional and
                                                    self.data_well.head_column_additional.get_value < self.data_well.current_bottom):
            self.nkt_select_combo.setCurrentIndex(0)
        else:

            self.nkt_select_combo.setCurrentIndex(1)

        self.paker_depth_label = QLabel("Глубина установки пакера", self)
        self.paker_depth_line = QLineEdit(self)
        self.paker_depth_line.setClearButtonEnabled(True)

        self.need_sand_filing_label = QLabel("Нужно ли отсыпать голову пакера", self)
        self.need_sand_filing_combo = QComboBox(self)
        self.need_sand_filing_combo.addItems(['Да', 'Нет'])

        self.roof_sand_label = QLabel("кровля ПМ", self)
        self.roof_sand_edit = QLineEdit(self)
        self.roof_sand_edit.setValidator(self.validator)

        self.roof_sand_edit.setText(f'{self.data_well.perforation_roof - 20}')
        self.roof_sand_edit.setClearButtonEnabled(True)

        self.type_work_label = QLabel("Вид работ", self)
        self.type_work_combo = QComboBox(self)
        self.type_work_combo.addItems(['установка', 'извлечение'])
        # self.sole_sand_edit.setText(f'{self.}')

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)

        # self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(1, 150)

        self.grid.addWidget(self.paker_type_label, 2, 1)
        self.grid.addWidget(self.paker_type_combo, 3, 1)

        self.grid.addWidget(self.pero_diameter_label, 2, 2)
        self.grid.addWidget(self.pero_diameter_line, 3, 2)

        self.grid.addWidget(self.nkt_select_label, 2, 3)
        self.grid.addWidget(self.nkt_select_combo, 3, 3)

        self.grid.addWidget(self.need_sand_filing_label, 4, 1)
        self.grid.addWidget(self.need_sand_filing_combo, 5, 1)

        self.grid.addWidget(self.roof_sand_label, 4, 3)
        self.grid.addWidget(self.roof_sand_edit, 5, 3)


        self.grid.addWidget(self.paker_depth_label, 7, 1)
        self.grid.addWidget(self.paker_depth_line, 8, 1)

        self.grid.addWidget(self.type_work_label, 9, 1, 1, 4)
        self.grid.addWidget(self.type_work_combo, 10, 1, 1, 4)

        self.type_work_combo.currentTextChanged.connect(self.update_type_work)


        self.type_work_combo.setCurrentIndex(1)

        if self.data_well.column_additional is False or \
                (self.data_well.column_additional and self.data_well.current_bottom < self.data_well.head_column_additional.get_value):
            self.nkt_select_combo.setCurrentIndex(1)
            self.nkt_select_combo.setCurrentIndex(0)
        else:
            self.nkt_select_combo.setCurrentIndex(1)

        if self.data_well.for_paker_list == True:
            self.type_work_combo.setCurrentIndex(1)
        else:
            self.type_work_combo.setCurrentIndex(0)

        self.paker_depth_line.textChanged.connect(self.update_depth_paker)



    def update_type_work(self, index):

        if index == 'установка':
            self.grid.addWidget(self.paker_type_label, 2, 1)
            self.grid.addWidget(self.paker_type_combo, 3, 1)

            self.grid.addWidget(self.pero_diameter_label, 2, 2)
            self.grid.addWidget(self.pero_diameter_line, 3, 2)

            self.grid.addWidget(self.nkt_select_label, 2, 3)
            self.grid.addWidget(self.nkt_select_combo, 3, 3)

            self.grid.addWidget(self.need_sand_filing_label, 4, 1)
            self.grid.addWidget(self.need_sand_filing_combo, 5, 1)

            self.grid.addWidget(self.roof_sand_label, 4, 3)
            self.grid.addWidget(self.roof_sand_edit, 5, 3)

            self.grid.addWidget(self.paker_depth_label, 7, 1)
            self.grid.addWidget(self.paker_depth_line, 8, 1)
            self.pero_diameter_label.setText('диаметр пакера')


            self.current_bottom_edit.setText(f'{self.data_well.current_bottom}')
            self.current_bottom_label.setParent(None)
            self.current_bottom_edit.setParent(None)
        else:

            self.current_bottom_edit.setText(f'{self.data_well.current_bottom}')
            self.grid.addWidget(self.current_bottom_label, 7, 3)
            self.grid.addWidget(self.current_bottom_edit, 8, 3)
            self.pero_diameter_label.setText('диаметр пера')
            if self.data_well.column_additional or self.data_well.column_additional is False and \
                    self.data_well.column_diameter.get_value < 130:
                self.pero_diameter_line.setText(f'{self.data_well.nkt_diam}')
            else:
                self.pero_diameter_line.setText(f'110')
            self.paker_type_label.setParent(None)
            self.paker_type_combo.setParent(None)
            self.need_sand_filing_label.setParent(None)
            self.need_sand_filing_combo.setParent(None)
            self.roof_sand_label.setParent(None)
            self.roof_sand_edit.setParent(None)
            if self.data_well.for_paker_list == True:

                self.paker_depth_line.setText(f'{data_list.depth_paker_izv}')
            self.current_bottom_edit.setText(str(self.data_well.current_bottom_second))

    def update_depth_paker(self):
        paker_depth = self.paker_depth_line.text()
        if paker_depth.isdigit():
            self.roof_sand_edit.setText(str(int(float(paker_depth))-20))
            self.pero_diameter_line.setText(str(self.paker_diameter_select(paker_depth)))

    def update_raid_edit(self, index):
        pass




class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSoPakerIzv(parent), 'извлекаемый пакер')


class PakerIzvlek(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)


        self.insert_index = data_well.insert_index
        self.tab_widget = TabWidget(self.data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)

        vbox = QGridLayout(self.centralWidget)

        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonadd_work, 3, 0)

    def closeEvent(self, event):
                # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия
    def add_work(self):
        type_work_combo = self.tab_widget.currentWidget().type_work_combo.currentText()
        pero_diameter_line = self.tab_widget.currentWidget().pero_diameter_line.text()
        nkt_key = self.tab_widget.currentWidget().nkt_select_combo.currentText()
        paker_depth_line = self.tab_widget.currentWidget().paker_depth_line.text()
        nkt_select_combo = self.tab_widget.currentWidget().nkt_select_combo.currentText()
        roof_sand_edit = int(float(self.tab_widget.currentWidget().roof_sand_edit.text()))

        paker_type_combo = self.tab_widget.currentWidget().paker_type_combo.currentText()
        sand_question = self.tab_widget.currentWidget().need_sand_filing_combo.currentText()

        if type_work_combo != 'установка':
            current_bottom = self.tab_widget.currentWidget().current_bottom_edit.text()
            if current_bottom != '':
                current_bottom = round(float(current_bottom), 1)

        if paker_depth_line != '':
            paker_depth_line = int(float(paker_depth_line))

        if nkt_select_combo == 'пакер в ЭК' and self.data_well.column_additional and \
                paker_depth_line > self.data_well.head_column_additional.get_value:
            QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка печати для доп колонны')
            return
        elif nkt_select_combo == 'пакер в ДП' and self.data_well.column_additional and \
                paker_depth_line < self.data_well.head_column_additional.get_value:
            QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка для основной колонны')
            return

        if type_work_combo == 'установка':
            if paker_depth_line == '':
                QMessageBox.warning(self, 'Ошибка',
                                          'Введите данные по глубине установки пакера')
                return

            if paker_depth_line > self.data_well.current_bottom:
                QMessageBox.warning(self, 'Ошибка',
                                          'Забой ниже глубины текущего забоя')
                return
            elif paker_depth_line == '' or pero_diameter_line == '':
                QMessageBox.warning(self, 'ПРОВЕРКА', 'Необходимо добавить глубину посадки пакера')
                return
            if self.data_well.column_additional and int(paker_depth_line) > self.data_well.head_column_additional.get_value and \
                    nkt_key == 'пакер в ЭК':
                QMessageBox.information(self, 'Внимание', 'Компоновка подобрана не корректно')
                return
            if self.data_well.column_additional and int(paker_depth_line) < self.data_well.head_column_additional.get_value \
                    and nkt_key == 'пакер в ДП':
                QMessageBox.information(self, 'Внимание', 'Компоновка подобрана не корректно')
                return

            if int(paker_depth_line) > self.data_well.current_bottom:
                QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                                       f'ниже текущего забоя')
                return
            if self.check_true_depth_template(paker_depth_line) is False:
                return
            if self.true_set_paker( paker_depth_line) is False:
                return
            if self.check_depth_in_skm_interval(paker_depth_line) is False:
                return


            raid_list = PakerIzvlek.rir_izvelPaker(
                self, paker_depth_line,  pero_diameter_line, paker_type_combo, sand_question, roof_sand_edit)
            self.calculate_chemistry("извлекаемый пакер", 1)
        else:
            raid_list = PakerIzvlek.izvlech_paker(self, pero_diameter_line, paker_depth_line, current_bottom)

        self.populate_row(self.insert_index, raid_list, self.table_widget)
        data_list.pause = False
        self.close()
        self.close_modal_forcefully()

    def rir_izvelPaker(self, paker_depth_line, pero_diameter_line, paker_type_combo, sand_question, roof_sand_edit):
        from work_py.template_work import TemplateKrs

        rir_list = [
            [f'СПО {paker_type_combo}-{pero_diameter_line} {TemplateKrs.calc_combo_nkt(self,"НКТ", paker_depth_line)} до глубины '
             f'{paker_depth_line}м',  None,
             f'Спустить пакер {paker_type_combo}-{pero_diameter_line} (извлекаемый) '
             f'{TemplateKrs.calc_combo_nkt(self,"НКТ", paker_depth_line)} на тНКТ до'
             f' глубины {paker_depth_line}м с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм.'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', lifting_nkt_norm(paker_depth_line, 1.2)],
            [f'Привязка', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через РИТС {data_list.contractor}". '
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [None, None,
             f'Произвести установку извлекаемого пакера на глубине {paker_depth_line}м по технологическому '
             f'плану работ плана '
             f'подрядчика.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4]
            ]


        if sand_question == 'Да':
            volume_sand = abs(round(
                well_volume(self, paker_depth_line) / paker_depth_line * 1000 * (paker_depth_line - roof_sand_edit), 0))

            filling_list = [
                [None, None,
                 f'Поднять ИУГ до глубины {roof_sand_edit - 120}м с доливом тех жидкости в '
                 f'объеме  {round(120 * 1.12 / 1000, 1)}м3 уд.весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4],
                [f'отсыпка в инт. {roof_sand_edit} - {paker_depth_line}  в объеме'
                 f' {round(well_volume(self, paker_depth_line) / paker_depth_line * 1000 * (20), 0)}л',
                 None, f'Произвести отсыпку кварцевым песком в инт. {roof_sand_edit} - {paker_depth_line} '
                       f' в объеме {volume_sand}л '
                       f'Закачать в НКТ кварцевый песок  с доводкой тех.жидкостью {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 3.5],
                [f'Ожидание 4 часа.', None, f'Ожидание оседания песка 4 часа.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 4],
                [None, None,
                 f'Допустить компоновку с замером и шаблонированием НКТ до кровли песчаного моста (плановый забой - '
                 f'{roof_sand_edit}м).'
                 f' Определить текущий забой скважины (перо от песчаного моста не поднимать, упереться в песчаный мост).',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.2],
                [None, None,
                 f'В случае если кровля песчаного моста на гл.{roof_sand_edit}м дальнейшие работы продолжить '
                 f'дальше по плану'
                 f'В случае пеcчаного моста ниже гл.{roof_sand_edit}м работы повторить с корректировкой объема и '
                 f'технологических глубин.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None],
                [None, None,
                 f'Поднять ИУГ с глубины {roof_sand_edit}м с доливом тех '
                 f'жидкости в объеме  {round(roof_sand_edit * 1.12 / 1000, 1)}м3 уд.весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4]]

            for row in filling_list:
                rir_list.append(row)
            self.data_well.current_bottom_second = self.data_well.current_bottom
            self.data_well.current_bottom = roof_sand_edit
            data_list.depth_paker_izv = paker_depth_line
            self.calculate_chemistry('песок', volume_sand)
        else:
            rir_list.append([None, None,
                             f'Поднять ИУГ c глубины {paker_depth_line}м с доливом тех жидкости в объеме '
                             f'{round(paker_depth_line * 1.12 / 1000, 1)}м3 уд.весом {self.data_well.fluid_work}',
                             None, None, None, None, None, None, None,
                             'Мастер КРС, подрядчик по ГИС', 4])
            self.data_well.current_bottom_second = self.data_well.current_bottom
            self.data_well.current_bottom = paker_depth_line

        self.data_well.for_paker_list = True
        data_list.depth_paker_izv = paker_depth_line
        return rir_list

    def izvlech_paker(self, pero_diameter_line, paker_depth_line, current_bottom):
        from work_py.template_work import TemplateKrs

        rir_list = [
            [f'СПО {RirWindow.pero_select(self, self.data_well.current_bottom).replace("перо", f"перо-{pero_diameter_line}мм")} до '
             f'глубины {round(self.data_well.current_bottom, 0)}м', None,
             f'Спустить {RirWindow.pero_select(self, self.data_well.current_bottom).replace("перо", f"перо-{pero_diameter_line}мм")}  '
             f'{TemplateKrs.calc_combo_nkt(self,"НКТ", paker_depth_line)} на НКТ{self.data_well.nkt_diam}мм до '
             f'глубины {round(self.data_well.current_bottom, 0)}м с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. '
             f'(При СПО первых десяти НКТ на '
             f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'Мастер КР', descentNKT_norm(self.data_well.current_bottom, 1)],
            [f'Вымыв песка до гл.{paker_depth_line - 10}',
             None,
             f'Произвести нормализацию забоя (вымыв кварцевого песка) с наращиванием, комбинированной промывкой '
             f'по круговой циркуляции '
             f'жидкостью  с расходом жидкости не менее 8 л/с до гл.{paker_depth_line-10}м. \n'
             f'Тех отстой 2ч. Повторное определение текущего забоя, при необходимости повторно вымыть.',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [None, None,
             f'Поднять {RirWindow.pero_select(self, self.data_well.current_bottom)} НКТ{self.data_well.nkt_diam}мм с глубины '
             f'{paker_depth_line - 10}м с доливом '
             f'скважины'
             f' в объеме {round((paker_depth_line - 10) * 1.12 / 1000, 1)}м3 тех. '
             f'жидкостью  уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', lifting_nkt_norm(paker_depth_line - 10, 1)]]

        emer_list = [
            [f'СПО лов. инст до до Н= {paker_depth_line-10}', None,
              f'Спустить с замером ловильный инструмент {TemplateKrs.calc_combo_nkt(self, "НКТ", paker_depth_line)} на '
              f'НКТ{self.data_well.nkt_diam} до Н= {paker_depth_line-10}м с замером. ',
              None, None, None, None, None, None, None,
              'мастер КРС', lifting_nkt_norm(self.data_well.current_bottom, 1)],
             [f'Вымыв песка до {paker_depth_line}м. Извлечение пакера', None,
              f'Произвести нормализацию (вымыв кварцевого песка) на ловильном инструменте до глубины '
              f'{paker_depth_line}м обратной '
              f'промывкой уд.весом {self.data_well.fluid_work} \n'
              f'Произвести  ловильный работы при представителе заказчика на глубине {paker_depth_line}м.',
              None, None, None, None, None, None, None,
              'мастер КРС', lifting_nkt_norm(paker_depth_line, 1)],
             [None, None,
              f'Расходить и поднять компоновку {TemplateKrs.calc_combo_nkt(self,"НКТ", paker_depth_line)} '
              f'НКТ{self.data_well.nkt_diam}мм с глубины {paker_depth_line}м с '
              f'доливом скважины в объеме {round(paker_depth_line * 1.12 / 1000, 1)}м3 тех. жидкостью '
              f'уд.весом {self.data_well.fluid_work}',
              None, None, None, None, None, None, None,
              'мастер КРС', lifting_nkt_norm(paker_depth_line, 1)]]
        for row in emer_list:
            rir_list.append(row)

        self.data_well.current_bottom = current_bottom
        self.data_well.for_paker_list = False
        return rir_list



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = PakerIzvlek(1 , 2)
    # window.show()
    sys.exit(app.exec_())
