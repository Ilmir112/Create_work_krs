from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLabel, QComboBox, QLineEdit, QGridLayout, QWidget, QPushButton, \
    QMainWindow, QTabWidget

from krs import volume_vn_ek, volume_vn_nkt, well_volume

from main import MyWindow
from work_py.alone_oreration import fluid_change
from work_py.drilling import drilling_nkt
from work_py.raiding import Raid
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm
from work_py.sand_filling import sandFilling, sand_select, sandWashing
from work_py.acid_paker import CheckableComboBox, AcidPakerWindow




class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        from open_pz import CreatePZ
        super().__init__(parent)


        self.paker_need_labelType = QLabel("необходимость спо пакера \nдля опрессовки ЭК и определения Q", self)
        self.paker_need_Combo = QComboBox(self)
        self.paker_need_Combo.addItems(['Нужно СПО', 'без СПО'])

        self.rir_type_Label = QLabel("Вид РИР", self)
        self.rir_type_Combo = QComboBox(self)
        self.rir_type_Combo.addItems(['РИР на пере', 'РИР с пакером', 'РИР с РПК', 'РИР с РПП'])

        plast_work = CreatePZ.plast_work
        if CreatePZ.leakiness:
            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                print(list(nek))
                nek1 = "-".join(map(str, list(map(int, list(nek)))))
                print(nek1)
                plast_work.append(f'НЭК {nek1}')

        self.plastLabel = QLabel("Выбор пласта", self)
        self.plastCombo = CheckableComboBox(self)
        self.plastCombo.combo_box.addItems(plast_work)
        self.plastCombo.combo_box.currentTextChanged.connect(self.update_plast_edit)


        self.roof_rir_label = QLabel("Плановая кровля РИР", self)

        self.roof_rir_Edit = QLineEdit(self)
        # self.roof_rir_Edit.setText()
        self.roof_rir_Edit.setClearButtonEnabled(True)

        self.sole_rir_LabelType = QLabel("Подошва РИР", self)

        self.sole_rir_Edit = QLineEdit(self)
        self.sole_rir_Edit.setClearButtonEnabled(True)
        # self.sole_rir_Edit.setText()
            # listEnabel = [self.khovstLabel, self.khvostEdit, self.swabTruelabelType, self.swabTrueEditType,
            #               self.plastCombo, self.pakerEdit, self.paker2Edit,
            #               self.svkTrueEdit, self.QplastEdit, self.skvProcEdit, self.acidEdit, self.acidVolumeEdit,
            #               self.acidProcEdit]
            # for enable in listEnabel:
            #     enable.setEnabled(False)

        grid = QGridLayout(self)

        grid.addWidget(self.paker_need_labelType, 4, 1)
        grid.addWidget(self.paker_need_Combo, 5, 1)

        grid.addWidget(self.rir_type_Label, 4, 2)
        grid.addWidget(self.rir_type_Combo,5, 2)
        grid.addWidget(self.plastLabel, 4, 3)
        grid.addWidget(self.plastCombo, 5, 3)
        grid.addWidget(self.roof_rir_label, 4, 4)
        grid.addWidget(self.roof_rir_Edit, 5, 4)
        grid.addWidget(self.sole_rir_LabelType, 4, 5)
        grid.addWidget(self.sole_rir_Edit, 5, 5)


    def update_plast_edit(self):
        from open_pz import CreatePZ
        dict_perforation = CreatePZ.dict_perforation

        plasts = CreatePZ.texts
        print(f'пласты {plasts, len(CreatePZ.texts), len(plasts), CreatePZ.texts}')
        roof_plast = CreatePZ.current_bottom
        sole_plast = 0
        for plast_sel in plasts:
            for plast in CreatePZ.plast_work:
                if plast_sel == plast:
                    try:
                        if roof_plast >= dict_perforation[plast]['кровля']:
                            roof_plast = dict_perforation[plast]['кровля']
                        if sole_plast <= dict_perforation[plast]['подошва']:
                            sole_plast = dict_perforation[plast]['подошва']
                    except:
                        pass
            # print(f' пл {plast_sel, roof_plast, sole_plast, CreatePZ.leakiness}')
            if CreatePZ.leakiness:
                for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                    # print(str(int(nek[0])), plast_sel, str(int(nek[0])) in plast_sel)
                    if str(int(nek[0])) in plast_sel:
                        if roof_plast >= nek[0]:

                            roof_plast = nek[0]
                            # print(f' кровля {roof_plast}')
                        if sole_plast <= nek[1]:
                            sole_plast = nek[1]
                        # print(nek, roof_plast, sole_plast)
        self.roof_rir_Edit.setText(f"{int(roof_plast - 30)}")
        self.sole_rir_Edit.setText(f"{CreatePZ.current_bottom}")

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Ремонтно-Изоляционные работы')


class RirWindow(QMainWindow):

    def __init__(self, table_widget, ins_ind, parent=None):

        super(QMainWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind


        self.tabWidget = TabWidget()


        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.addRowTable)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def rir_rpp(self, paker_need_Combo, plastCombo, roof_rir_Edit):
        from open_pz import CreatePZ
        from work_py.opressovka import paker_list

        rir_list = []

        rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
        if rir_rpk_question == QMessageBox.StandardButton.Yes:
            rir_rpk_plast_true = True
        else:
            rir_rpk_plast_true = False

        roof_rir_Edit = MyWindow.true_set_Paker(self, roof_rir_Edit)

        if paker_need_Combo == 'Нужно СПО':
            for row in paker_list(self):
             rir_list.append(row)
        else:
            rir_list = []
        nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])

        rir_work_list = [[f'СПО РПП до глубины {roof_rir_Edit}м', None,
                       f'Спустить   пакер глухой {self.rpk_nkt(roof_rir_Edit)}  на тНКТ{nkt_diam}мм '
                       f'до глубины {roof_rir_Edit}м '
                       f'с замером, шаблонированием шаблоном. '
                       f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
                       f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии '
                       f'представителя РИР или УСРСиСТ.',
            None, None, None, None, None, None, None,
        'мастер КРС', descentNKT_norm(roof_rir_Edit,1.2)],
         [f'Привязка по ГК и ЛМ', None,
          f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
          f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
          f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик по ГИС', 4],
         [f'опрессовать НКТ на 200атм', None,
          f'При наличии циркуляции опрессовать НКТ на 200атм '
          f'в присутствии порядчика по РИР. Составить акт. Вымыть шар обратной промывкой ',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.5+0.6],
         [f'установка РПП на {roof_rir_Edit}м', None,
          f'Произвести установку глухого пакера  для изоляции {plastCombo} по технологическому плану подрядчика по РИР силами подрядчика по РИР '
          f'с установкой пакера  на глубине {roof_rir_Edit}м',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],

         [f'{"".join([f"Опрессовать на Р={CreatePZ.max_admissible_pressure}атм" if  rir_rpk_plast_true == False else ""])}',
          None,
          f'{"".join([f"Опрессовать эксплуатационную колонну на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика" if  rir_rpk_plast_true == False else ""])} '
          f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
         [None, None,
          f'Поднять стыковочное устройство с глубины {roof_rir_Edit}м с доливом скважины в объеме '
          f'{round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work} ',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_Edit, 1.2)]]


        for row in rir_work_list:
            rir_list.append(row)

        CreatePZ.current_bottom = roof_rir_Edit
        self.perf_new(roof_rir_Edit, roof_rir_Edit + 1)
        return rir_list



    def rir_rpk(self, paker_need_Combo, plastCombo, roof_rir_Edit):
        from open_pz import CreatePZ
        from work_py.opressovka import paker_list, paker_diametr_select
        rir_list = []

        rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')

        if rir_rpk_question == QMessageBox.StandardButton.Yes:
            rir_rpk_plast_true = True
        else:
            rir_rpk_plast_true = False

        roof_rir_Edit = MyWindow.true_set_Paker(self, roof_rir_Edit)

        if paker_need_Combo == 'Нужно СПО':
            for row in paker_list(self):
                rir_list.append(row)

        nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])

        if rir_rpk_plast_true:
            rir_q_list = [[f'Привязка по ГК и ЛМ', None,
          f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
          f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г.'
          f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик по ГИС', 4],
          [f'посадить пакер на глубину {roof_rir_Edit}м'
              , None,
                       f'посадить пакер на глубину {roof_rir_Edit}м',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 1],
          [f'Насыщение 5м3. Определить приемистость {plastCombo} при Р=80-100атм',
           None,
                       f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plastCombo} при Р=80-100атм '
                       f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                       f'после закачки, объем согласовать с подрядчиком по РИР). В случае приёмистости менее  250м3/сут '
                       f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
                       f'приемистости по технологическому плану',
            None, None, None, None, None, None, None,
            'мастер КРС', 1.35]]
            for row in rir_q_list:
                rir_list.insert(-1, row)
        else:
            rir_rpk_plast_true = False

            rir_q_list = [
                          [f'Насыщение 5м3. Определить Q {plastCombo} при Р=80-100атм',
                           None,
                           f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plastCombo} при Р=80-100атм '
                           f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                           f'после закачки, объем согласовать с подрядчиком по РИР). В случае приёмистости менее  250м3/сут '
                           f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
                           f'приемистости по технологическому плану',
                           None, None, None, None, None, None, None,
                           'мастер КРС', 1.35]]
            for row in rir_q_list[::-1]:
                rir_list.insert(-1, row)

        rir_work_list = [[f'СПО пакера РПК до глубины {roof_rir_Edit}м', None,
                       f'Спустить   пакера РПК {self.rpk_nkt(roof_rir_Edit)}  на тНКТ{nkt_diam}мм до глубины {roof_rir_Edit}м с '
                       f'замером, шаблонированием шаблоном. '
                       f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
                       f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии представителя '
                       f'РИР или УСРСиСТ.',
            None, None, None, None, None, None, None,
        'мастер КРС', descentNKT_norm(roof_rir_Edit,1.2)],
         [f'Привязкапо ГК и ЛМ', None,
          f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
          f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
          f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик по ГИС', 4],
         [f'опрессовать НКТ на 200атм', None,
          f'При наличии циркуляции опрессовать НКТ на 200атм '
          f'в присутствии порядчика по РИР. Составить акт. Вымыть шар обратной промывкой ',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
         [f'РИР {plastCombo} с установкой пакера РПК на глубине {roof_rir_Edit}м ', None,
          f'Произвести РИР {plastCombo} по технологическому плану подрядчика по РИР силами подрядчика по РИР '
          f'с установкой пакера РПК на глубине {roof_rir_Edit}м',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
         [f'ОЗЦ 16-24 часа', None,
          f'ОЗЦ 16-24 часа: (по качеству пробы) с момента отстыковки пакера В случае не получения '
          f'технологического "СТОП" ОЗЦ без давления.',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 16],
         [f'{"".join([f"Опрессовать на Р={CreatePZ.max_admissible_pressure}атм" if rir_rpk_plast_true == False else ""])}',
          None,
          f'{"".join([f"Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика" if rir_rpk_plast_true == False else ""])} '
          f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ',0.67],
         [None, None,
          f'Во время ОЗЦ поднять стыковочное устройство с глубины {roof_rir_Edit}м с доливом скважины в объеме '
          f'{round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work} ',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_Edit,1)]]
        for row in rir_work_list:
            rir_list.append(row)
        self.perf_new(roof_rir_Edit, CreatePZ.current_bottom)
        CreatePZ.current_bottom = roof_rir_Edit

        return rir_list

    def perf_new(self, roofRir, solePir):

        from open_pz import CreatePZ

        print(f' пласта до изоляции {CreatePZ.plast_work}')
        CreatePZ.perforation_roof = 5000
        CreatePZ.perforation_sole = 0

        for plast in CreatePZ.plast_all:
            for interval in list((CreatePZ.dict_perforation[plast]['интервал'])):
                if roofRir <= interval[0] <= solePir:
                    CreatePZ.dict_perforation[plast]['отключение'] = True
                if CreatePZ.dict_perforation[plast]['отключение'] == False:
                    if interval[0] < CreatePZ.perforation_roof:
                        CreatePZ.perforation_roof = interval[0]
                    elif interval[1] > CreatePZ.perforation_sole:
                        CreatePZ.perforation_sole = interval[1]
        print(f' Подошва ПВР {CreatePZ.perforation_sole}')

        CreatePZ.plast_work = []
        for plast in CreatePZ.plast_all:
            if CreatePZ.dict_perforation[plast]['отключение'] == False:
                CreatePZ.plast_work.append(plast)

        if len(CreatePZ.dict_leakiness) != 0:
            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                print(roofRir, float(nek[0]), solePir)
                if roofRir <= float(nek[0]) <= solePir:
                    CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отключение'] = True
            print(f"при {CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отключение']}")

        print(CreatePZ.dict_leakiness)

        print(f' пласта рабоче {CreatePZ.plast_work}')
        CreatePZ.definition_plast_work(self)



    def rpk_nkt(self, paker_depth):
        from open_pz import CreatePZ
        from work_py.opressovka import nktOpress
        CreatePZ.nktOpressTrue = False


        if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth< CreatePZ.head_column_additional:
            rpk_nkt_select = f' для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм ' \
                           f'+ {nktOpress(self)[0]} + НКТ + репер'
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth> CreatePZ.head_column_additional:
            rpk_nkt_select = f' для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]} ' \
                           f'+ НКТ60мм + репер + НКТ60мм L- {round(paker_depth-CreatePZ.head_column_additional, 0)}м '
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth> CreatePZ.head_column_additional:
            rpk_nkt_select = f' для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]}' \
                           f'+ НКТ + репер + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками L- {round(paker_depth-CreatePZ.head_column_additional, 0)}м '

        return rpk_nkt_select


    def rirWithPero(self, paker_need_Combo, plastCombo, roof_rir_Edit, sole_rir_Edit):
        from open_pz import CreatePZ
        from work_py.opressovka import paker_list, paker_diametr_select
        from krs import volume_vn_nkt

        nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])

        
        if CreatePZ.column_additional == True and CreatePZ.column_additional_diametr <110:
            dict_nkt = {73: CreatePZ.head_column_additional, 60: CreatePZ.head_column_additional-sole_rir_Edit}
        else:
            dict_nkt = {73: sole_rir_Edit}


        volume_cement = round(volume_vn_ek(self,roof_rir_Edit) * (sole_rir_Edit - roof_rir_Edit)/1000, 1)

        uzmPero_list = [
            [f' СПО пера до глубины {sole_rir_Edit}м Опрессовать НКТ на 200атм', None,
             f'Спустить {self.pero_select(sole_rir_Edit)}  на тНКТ{nkt_diam}мм до глубины {sole_rir_Edit}м с '
             f'замером, шаблонированием '
             f'шаблоном. Опрессовать НКТ на 200атм. Вымыть шар. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС',descentNKT_norm(sole_rir_Edit, 1)],
            [f'УЦМ в интервале {roof_rir_Edit}-{sole_rir_Edit}м', None,
             f'Произвести установку  цементного моста в интервале {roof_rir_Edit}-{sole_rir_Edit}м в присутствии '
             f'представителя УСРСиСТ',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [None, None,
             f'Приготовить цементный раствор у=1,82г/см3 в объёме {volume_cement}м3'
             f' (сухой цемент{round(volume_cement*1.25,1)}т) ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме 0,5м3, цементный '
             f'раствор в объеме {volume_cement}м3, '
             f'довести тех.жидкостью у=1,00г/см3 в объёме 1,5м3, тех. жидкостью  в '
             f'объёме {round(volume_vn_nkt(dict_nkt)-1.5,1)}м3. '
             f'Уравновешивание цементного раствора',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Приподнять перо до гл.{roof_rir_Edit}м. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Открыть трубное пространство. Промыть скважину обратной промывкой (срезка) по круговой циркуляции '
             f'тех.жидкостью  в объеме не менее {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 уд.весом {CreatePZ.fluid_work} (Полуторакратный объем НКТ) '
             f'с расходом жидкости 8л/с (срезка) до чистой воды.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(16)],
            [None, None,
             f'Поднять перо на безопасную зону до гл. {roof_rir_Edit-300}м с доливом скважины в объеме 0,3м3 тех. жидкостью '
             f'уд.весом {CreatePZ.fluid_work}.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [f'ОЗЦ - 23 час', None,
             f'ОЗЦ - 23 часа (с момента завершения срезки цементного раствора - 24 часа (по качеству пробы))) \n'
             f'ОЗЦ без давления.',
             None, None, None, None, None, None, None,
             'мастер КРС',24],
            [None, None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста (плановый на гл. {roof_rir_Edit}м'
             f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной телефонограммой.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [f'Опрессовать на Р={CreatePZ.max_admissible_pressure}атм',
             None,
             f'Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя '
             f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
             f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
             f'В случае головы ЦМ ниже планового РИР повторить  с учетом корректировки мощности моста ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.67],
            [None, None,
             f'Поднять перо на тНКТ{nkt_diam}мм с глубины {roof_rir_Edit}м с доливом скважины в объеме 2,2м3 тех. жидкостью '
             f'уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(roof_rir_Edit, 1)],
        ]


        if len(CreatePZ.plast_work) == 0:
            rir_list = []
            for row in uzmPero_list:
                rir_list.append(row)

            self.perf_new(roof_rir_Edit, sole_rir_Edit)
            CreatePZ.current_bottom = roof_rir_Edit

            if len(CreatePZ.plast_work) != 0:
                rir_list.pop(-2)

        else:
            rir_list = []
            rirPero_list = [
                [f'СПО пера до глубины {sole_rir_Edit}м. Опрессовать НКТ на 200атм', None,
                 f'Спустить {self.pero_select(sole_rir_Edit)}  на тНКТ{nkt_diam}мм до глубины {sole_rir_Edit}м '
                 f'с замером, шаблонированием '
                 f'шаблоном. Опрессовать НКТ на 200атм. Вымыть шар. \n'
                 f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(sole_rir_Edit, 1)],
                [f'УЦМ в инт {roof_rir_Edit}-{sole_rir_Edit}м',
                 None,
                 f'Произвести цементную заливку с целью изоляции пласта {plastCombo}  в интервале '
                 f'{roof_rir_Edit}-{sole_rir_Edit}м в присутствии '
                 f'представителя УСРС и СТ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 2.5],
                [None, None,
                 f'Приготовить цементный раствор у=1,82г/см3 в объёме {volume_cement}м3'
                 f' (сухой цемент{round(volume_cement * 1.25, 1)}т) ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.5],
                [None, None,
                 f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме 0,5м3, цементный раствор в '
                 f'объеме {volume_cement}м3, '
                 f'довести тех.жидкостью у=1,00г/см3 в объёме 1,5м3, тех. жидкостью  в объёме '
                 f'{round(volume_vn_nkt(dict_nkt) - 1.5, 1)}м3. '
                 f'Уравновешивание цементного раствора',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.5],
                [None, None,
                 f'Приподнять перо до гл.{roof_rir_Edit}м. Закрыть трубное простанство. '
                 f'Продавить по затрубному пространству '
                 f'тех.жидкостью  при давлении не более {CreatePZ.max_admissible_pressure}атм '
                 f'(до получения технологического СТОП).',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.5],
                [None, None,
                 f'Открыть трубное пространство. Промыть скважину обратной промывкой (срезка) по круговой циркуляции '
                 f'тех.жидкостью  в объеме не менее {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 уд.весом '
                 f'{CreatePZ.fluid_work} '
                 f'(Полуторакратный объем НКТ) '
                 f'с расходом жидкости 8л/с (срезка) до чистой воды.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', well_volume_norm(16)],
                [None, None,
                 f'Поднять перо на безопасную зону до гл. {roof_rir_Edit - 300}м с доливом скважины в объеме 0,3м3 тех. жидкостью '
                 f'уд.весом {CreatePZ.fluid_work}.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.2],
                [None, None,
                 f'ОЗЦ - 23 часа (с момента завершения срезки цементного раствора - 24 часа (по качеству пробы))) \n'
                 f'ОЗЦ без давления.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 24],
                [None, None,
                 f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста '
                 f'(плановый на гл. {roof_rir_Edit}м'
                 f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной '
                 f'телефонограммой.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.2],
                [f'Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм',
                 None,
                 f'Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя '
                 f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                 f'с подтверждением за 2 часа до '
                 f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
                 f'В случае головы ЦМ ниже планового РИР повторить  с учетом корректировки мощности моста ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.67],
                [None, None,
                 f'Поднять перо на тНКТ{nkt_diam}мм с глубины {roof_rir_Edit}м с доливом скважины в объеме '
                 f'{round(roof_rir_Edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
                 f'уд.весом {CreatePZ.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(roof_rir_Edit, 1)],
            ]
            if paker_need_Combo == 'Нужно СПО':
                for row in paker_list(self):
                    rir_list.append(row)


                glin_list = [
                    [f'насыщение 5м3. Определить Q {plastCombo} при Р=80-100атм ',
                     None,
                     f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plastCombo} при Р=80-100атм '
                     f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                     f'после закачки, объем согласовать с подрядчиком по РИР). В случае приёмистости менее  250м3/сут '
                     f'при Р={CreatePZ.max_admissible_pressure}атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
                     f'приемистости по технологическому плану',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 1.77],
                    [None, None,
                     f'По результатам определения приёмистости выполнить следующие работы: \n'
                     f'В случае приёмистости свыше 480 м3/сут при Р=100атм выполнить работы по закачке гдинистого раствора '
                     f'(по согласованию с ГС и ПТО ООО Ойл-сервис и заказчика). \n'
                     f'В случае приёмистости менее 480 м3/сут при Р=100атм и более 120м3/сут при Р=100атм приступить к выполнению РИР',
                     None, None, None, None, None, None, None,
                     'мастер КРС, заказчик', None],
                    [None, None,
                     f'Объём глинистого р-ра скорректировать на устье на основании тех.возможности. \n'
                     f'Приготовить глинистый раствор в объёме 5м3 (расчет на 1 м3 - сухой глинопорошок массой 0,3т + '
                     f'вода у=1,00г/см3 в объёме 0,9м3) плотностью у=1,24г/см3',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 3.5],
                    [f'Закачка глины для сбития приемистости', None,
                     f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в объеме 5м3 + тех. воду '
                     f'в объёме {round(volume_vn_nkt(dict_nkt) - 5,1)}м3. Закрыть затруб. '
                     f'Продавить в НКТ тех. воду  в объёме {volume_vn_nkt(dict_nkt)}м3 при давлении не более '
                     f'{CreatePZ.max_admissible_pressure}атм.',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 0.5],
                    [f'Коагуляция 4 часа', None,
                     f'Коагуляция 4 часа (на основании конечного давления при продавке. '
                     f'В случае конечного давления менее 50атм, согласовать объем глинистого раствора с '
                     f'Заказчиком и продолжить приготовление следующего объема глинистого объема).',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 4],
                    [None, None,
                     f'Определить приёмистость по НКТ при Р=100атм.',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 0.35],
                    [None, None,
                     f'В случае необходимости выполнить работы по закачке глнистого раствора, с корректировкой '
                     f'по объёму раствора.',
                     None, None, None, None, None, None, None,
                     'мастер КРС', None ],
                    [None, None,
                     f'Промыть скважину обратной промывкой по круговой циркуляции  жидкостью '
                     f'в объеме не менее {well_volume(self, volume_vn_nkt(dict_nkt))}м3 с расходом жидкости не менее 8 л/с.',
                     None, None, None, None, None, None, None,
                     'мастер КРС', well_volume_norm(24)]
                ]
                if volume_vn_nkt(dict_nkt) <= 5:
                    glin_list[3] = [None, None,
                                    f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в '
                                    f'объеме {volume_vn_nkt(dict_nkt)}м3. Закрыть затруб. '
                                    f'Продавить в НКТ остаток глинистого раствора в объеме '
                                    f'{round(5 - volume_vn_nkt(dict_nkt), 1)} и тех. воду  в объёме '
                                    f'{volume_vn_nkt(dict_nkt)}м3 при давлении не более {CreatePZ.max_admissible_pressure}атм.',
                                    None, None, None, None, None, None, None,
                                    'мастер КРС', 0.5]

                for row in glin_list:
                    rir_list.insert(-3, row)
            else:
                rir_list = []

            for row in rirPero_list:
                rir_list.append(row)
            self.perf_new(roof_rir_Edit, CreatePZ.current_bottom)
            CreatePZ.current_bottom = roof_rir_Edit

            if len(CreatePZ.plast_work) != 0:
                rir_list.pop(-2)
            else:
                acid_true_quest = QMessageBox.question(self, 'Необходимость смены объема',
                                                       'Нужно ли изменять удельный вес?')
                if acid_true_quest == QMessageBox.StandardButton.Yes:
                    for row in fluid_change(self):
                        rir_list.insert(-1, row)

        return rir_list

    def pero_select(self, sole_rir_Edit):
        from open_pz import CreatePZ
        if CreatePZ.column_additional == False or CreatePZ.column_additional == True and sole_rir_Edit < CreatePZ.head_column_additional:
            pero_select = f'перо + опрессовочное седло + НКТ{CreatePZ.nkt_diam} 20м + репер'

        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and sole_rir_Edit > CreatePZ.head_column_additional:
            pero_select = f'перо + опрессовочное седло + НКТ60мм 20м + репер + НКТ60мм L- {round(sole_rir_Edit - CreatePZ.head_column_additional, 1)}м'
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and sole_rir_Edit > CreatePZ.head_column_additional:
            pero_select = f'воронку + опрессовочное седло + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками 20м + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками' \
                           f' L- {sole_rir_Edit - CreatePZ.head_column_additional}м'
        return pero_select

    def rir_paker(self, paker_need_Combo, plastCombo, roof_rir_Edit, sole_rir_Edit):
        from open_pz import CreatePZ
        from work_py.opressovka import paker_list
        rir_list = []
        for row in paker_list(self):
            rir_list.append(row)

        rir_q_list = [f'насыщение 5м3. Определить Й {plastCombo} при Р=80-100атм. СКВ', None,
               f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plastCombo} при Р=80-100атм '
               f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
               f'после закачки, объем согласовать с подрядчиком по РИР). В случае приёмистости менее  250м3/сут '
               f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
               f'приемистости по технологическому плану',
               None, None, None, None, None, None, None,
               'мастер КРС', 1.77]
        rir_list.insert(-3, rir_q_list)

        rir_paker_list = [[ f'РИР c пакером {plastCombo} c плановой кровлей на глубине {roof_rir_Edit}м',
                            None,
          f'Произвести РИР {plastCombo} c плановой кровлей на глубине {roof_rir_Edit}м по технологическому плану'
          f' подрядчика по РИР силами подрядчика по РИР '
          f'Перед спуском технологического пакера произвести испытание гидроякоря в присутсвии представителя '
          f'РИР или УСРСиСТ.',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
         [f'ОЗЦ 16-24 часа', None,
          f'ОЗЦ 16-24 часа: (по качеству пробы) с момента отстыковки пакера В случае не получения '
          f'технологического "СТОП" ОЗЦ без давления.',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 24],
          [f'Определение кровли', None,
           f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста (плановый на '
           f'гл. {roof_rir_Edit}м'
           f' с прямой промывкой и разгрузкой на забой 3т',
           None, None, None, None, None, None, None,
           'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
         [f'Опрессовать на Р={CreatePZ.max_admissible_pressure}атм', None,
          f'Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика '
          f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала '
          f'работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком.',
          None, None, None, None, None, None, None,
          'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
          [None, None,
           f'Поднять компоновку РИР на тНКТ{CreatePZ.nkt_diam}мм с глубины {roof_rir_Edit}м с доливом скважины в объеме '
           f'{round(roof_rir_Edit * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
           None, None, None, None, None, None, None,
           'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_Edit,1.2)]
            ]
        self.perf_new(roof_rir_Edit, CreatePZ.current_bottom)
        CreatePZ.current_bottom = roof_rir_Edit

        if len(CreatePZ.plast_work) != 0:
            rir_paker_list.pop(-2)
        for row in rir_paker_list:
            rir_list.append(row)
        return rir_list

    def addRowTable(self):
        from open_pz import CreatePZ

        plastCombo = str(self.tabWidget.currentWidget().plastCombo.combo_box.currentText())
        paker_need_Combo = str(self.tabWidget.currentWidget().paker_need_Combo.currentText())
        rir_type_Combo = str(self.tabWidget.currentWidget().rir_type_Combo.currentText())
        roof_rir_Edit = int(float(self.tabWidget.currentWidget().roof_rir_Edit.text().replace(',', '.')))
        sole_rir_Edit = int(float(self.tabWidget.currentWidget().sole_rir_Edit.text().replace(',', '.')))

        if rir_type_Combo == 'РИР на пере': # ['РИР на пере', 'РИР с пакером', 'РИР с РПК', 'РИР с РПП']

            work_list = self.rirWithPero(paker_need_Combo, plastCombo, roof_rir_Edit, sole_rir_Edit)
            AcidPakerWindow.populate_row(self, CreatePZ.ins_ind, work_list)

        elif rir_type_Combo == 'РИР с пакером': # ['РИР на пере', 'РИР с пакером', 'РИР с РПК', 'РИР с РПП']
            print(paker_need_Combo, plastCombo, roof_rir_Edit, sole_rir_Edit)
            work_list = self.rir_paker(paker_need_Combo, plastCombo, roof_rir_Edit, sole_rir_Edit)
            AcidPakerWindow.populate_row(self, CreatePZ.ins_ind, work_list)
        elif rir_type_Combo == 'РИР с РПК': # ['РИР на пере', 'РИР с пакером', 'РИР с РПК', 'РИР с РПП']

            work_list = self.rir_rpk(paker_need_Combo, plastCombo, roof_rir_Edit)
            AcidPakerWindow.populate_row(self, CreatePZ.ins_ind, work_list)
        elif rir_type_Combo == 'РИР с РПП': # ['РИР на пере', 'РИР с пакером', 'РИР с РПК', 'РИР с РПП']

            work_list = self.rir_rpp(paker_need_Combo, plastCombo, roof_rir_Edit)
            AcidPakerWindow.populate_row(self, CreatePZ.ins_ind, work_list)

        CreatePZ.pause = True
        self.close()
    def rir_izvelPaker(self):
        from open_pz import CreatePZ
        pakerIzvPaker, ok = QInputDialog.getInt(None, 'Глубина извлекаемого пакера',
                                          'Введите глубину установки извлекаемого пакера ',
                                          int(CreatePZ.perforation_roof-50), 0, int(CreatePZ.bottomhole_drill))

        pakerIzvPaker = MyWindow.true_set_Paker(self, pakerIzvPaker)

        CreatePZ.pakerIzvPaker = pakerIzvPaker
        rir_list = [[f'СПО пакера извлекаемый до глубины {pakerIzvPaker}м',
                     None,
           f'Спустить  пакера извлекаемый компании НЕОИНТЕХ +НКТ 20м + реперный патрубок 2м на тНКТ до'
           f' глубины {pakerIzvPaker}м с замером, шаблонированием шаблоном 59,6мм.'
           f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
           None, None, None, None, None, None, None,
           'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(pakerIzvPaker,1.2)],
        [f'Привязка', None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
         f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 4],
        [None, None,
         f'Произвести установку извлекаемого пакера на глубине {pakerIzvPaker}м по технологическому плану работ плана '
         f'подрядчика.',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 4 ],
        [None, None,
         f'Поднять ИУГ с доливом тех жидкости в объеме  {round(pakerIzvPaker * 1.12 / 1000, 1)}м3 уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 4]]
        CreatePZ.current_bottom2 = CreatePZ.current_bottom

        filling_list = [
            [None, None,
             f' Спустить  {sand_select(self)}  на НКТ{CreatePZ.nkt_diam}мм до глубины {round(pakerIzvPaker - 100, 0)}м '
             f'с замером, шаблонированием шаблоном. (При СПО первых десяти НКТ на '
             f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'Мастер КР', descentNKT_norm(CreatePZ.current_bottom, 1)],
            [f'отсыпка в инт. {pakerIzvPaker-20} - {pakerIzvPaker}  в объеме'
             f' {round(well_volume(self, pakerIzvPaker) / pakerIzvPaker * 1000 * (20), 0)}л',
             None, f'Произвести отсыпку кварцевым песком в инт. {pakerIzvPaker-20} - {pakerIzvPaker} '
                 f' в объеме {round(well_volume(self, pakerIzvPaker) / pakerIzvPaker * 1000 * (20), 0)}л '
                 f'Закачать в НКТ кварцевый песок  с доводкой тех.жидкостью {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [f'Ожидание 4 часа.', None, f'Ожидание оседания песка 4 часа.',
             None, None, None, None, None, None, None,
             'мастер КРС', 4],
            [None, None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли песчаного моста (плановый забой - '
             f'{pakerIzvPaker-20}м).'
             f' Определить текущий забой скважины (перо от песчаного моста не поднимать, упереться в песчаный мост).',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],

            [None, None,
             f'В случае если кровля песчаного моста на гл.{pakerIzvPaker-20}м дальнейшие работы продолжить дальше по плану'
             f'В случае пеcчаного моста ниже гл.{pakerIzvPaker-20}м работы повторить с корректировкой обьема и '
             f'технологических глубин.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Поднять {sand_select(self)} НКТ{CreatePZ.nkt_diam}мм с глубины {pakerIzvPaker-20 }м с доливом скважины в '
             f'объеме {round(pakerIzvPaker * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(pakerIzvPaker, 1)]
        ]

        sand_question = QMessageBox.question(None, 'Отсыпка', 'Нужна ли отсыпка головы пакера?')
        if sand_question == QMessageBox.StandardButton.Yes:
            for row in filling_list:
                rir_list.append(row)
            CreatePZ.current_bottom = pakerIzvPaker-20

        else:
            CreatePZ.current_bottom = pakerIzvPaker

        return rir_list

    def izvlech_paker(self):
        from open_pz import CreatePZ
        rir_list = [[f'СПО {sand_select(self).replace("перо", "перо-110мм")} до '
                     f'глубины {round(CreatePZ.current_bottom,0)}м', None,
         f' Спустить  {sand_select(self).replace("перо", "перо-110мм")}  на НКТ{CreatePZ.nkt_diam}мм до '
         f'глубины {round(CreatePZ.current_bottom,0)}м с замером, шаблонированием шаблоном. '
         f'(При СПО первых десяти НКТ на '
         f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'Мастер КР', descentNKT_norm(CreatePZ.current_bottom, 1)],
            [f'Вымыв песка до гл.{CreatePZ.pakerIzvPaker-10}',
             None, f'Произвести нормализацию забоя (вымыв кварцевого песка) с наращиванием, комбинированной промывкой '
                   f'по круговой циркуляции '
                 f'жидкостью  с расходом жидкости не менее 8 л/с до гл.{CreatePZ.pakerIzvPaker-10}м. \n'
                 f'Тех отстой 2ч. Повторное определение текущего забоя, при необходимости повторно вымыть.',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [None, None,
             f'Поднять {sand_select(self)} НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.pakerIzvPaker-10}м с доливом '
             f'скважины'
             f' в объеме {round((CreatePZ.pakerIzvPaker-10) * 1.12 / 1000, 1)}м3 тех. '
             f'жидкостью  уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(CreatePZ.pakerIzvPaker-10, 1)]]

        emer_list = [[f'СПО лов. инст до до Н= {CreatePZ.current_bottom}', None,
             f'Спустить с замером ловильный инструмент на НКТ до Н= {CreatePZ.current_bottom}м с замером. ',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(CreatePZ.current_bottom, 1)],
                     [f'Вымыв песка до {CreatePZ.pakerIzvPaker}м. Извлечение пакера', None,
                      f'Произвести нормализацию (вымыв кварцевого песка) на ловильном инструменте до глубины '
                      f'{CreatePZ.pakerIzvPaker}м обратной '
                      f'промывкой уд.весом {CreatePZ.fluid_work} \n'
                      f'Произвести  ловильный работы при представителе заказчика на глубине {CreatePZ.pakerIzvPaker}м.',
                      None, None, None, None, None, None, None,
                      'мастер КРС', liftingNKT_norm(CreatePZ.pakerIzvPaker, 1)],
                     [None, None,
                      f'Рассхадить и поднять компоновку НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.pakerIzvPaker}м с '
                      f'доливом скважины в объеме {round(CreatePZ.pakerIzvPaker * 1.12 / 1000, 1)}м3 тех. жидкостью '
                      f'уд.весом {CreatePZ.fluid_work}',
                      None, None, None, None, None, None, None,
                      'мастер КРС', liftingNKT_norm(CreatePZ.pakerIzvPaker, 1)]]
        for row in emer_list:
            rir_list.append(row)

        CreatePZ.current_bottom = CreatePZ.current_bottom2
        return rir_list
