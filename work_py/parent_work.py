from datetime import datetime

from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QTabWidget

from main import MyMainWindow
from data_list import contractor


class TabPageUnion(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.validator_float = QDoubleValidator(0.0, 8000.0, 2)
        self.validator_int = QIntValidator(0, 8000)
        self.dict_data_well = parent

    @staticmethod
    def if_None(value):
        if isinstance(value, datetime):
            return value
        elif value is None or 'отс' in str(value).lower() or str(value).replace(' ', '') == '-' \
                or value == 0 or str(value).replace(' ', '') == '':
            return 'отсут'
        else:
            return value



class TabWidgetUnion(QTabWidget):
    def __init__(self, parent=None):
        super().__init__()


class WindowUnion(MyMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.dict_data_well = parent

    def pvo_gno(self, kat_pvo):
        if 'Ойл' in contractor:
            date_str = 'от 07.03.2024г'
        elif 'РН' in contractor:
            date_str = ''
        # print(f' ПВО {kat_pvo}')
        pvo_2 = f'Установить ПВО по схеме №2 утвержденной главным инженером {contractor} {date_str} (тип плашечный ' \
                f'сдвоенный ПШП-2ФТ-152х21) и посадить пакер. ' \
                f'Спустить пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) и линии манифольда до концевых ' \
                f'задвижек на Р-{self.dict_data_well["max_admissible_pressure"]._value}атм на максимально допустимое давление ' \
                f'опрессовки эксплуатационной колонны в течении ' \
                f'30мин), сорвать пакер. ' \
            # f'В случае невозможности опрессовки по ' \
        # f'результатам определения приемистости и по согласованию с заказчиком  опрессовать трубные плашки ПВО на ' \
        # f'давление поглощения, но не менее 30атм. '

        pvo_1 = f'Установить ПВО по схеме №2 утвержденной главным инженером {contractor} {date_str} ' \
                f'(тип плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
                f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
                f' (при необходимости произвести монтаж переводника' \
                f' П178х168 или П168 х 146 или ' \
                f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки). Спустить и посадить ' \
                f'пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) на ' \
                f'Р-{self.dict_data_well["max_admissible_pressure"]._value}атм ' \
                f'(на максимально допустимое давление опрессовки ' \
                f'эксплуатационной колонны в течении 30мин), сорвать и извлечь пакер. Опрессовать ' \
                f'выкидную линию после концевых задвижек на ' \
                f'Р - 50 кгс/см2 (5 МПа) - для противовыбросового оборудования, рассчитанного на' \
                f'давление до 210 кгс/см2 ((21 МПа)\n' \
                f'- Обеспечить обогрев превентора и СУП в зимнее время . \n Получить разрешение на производство работ в ' \
                f'присутствии представителя ПФС'
        if kat_pvo == 1:
            return pvo_1, f'Монтаж ПВО по схеме №2 + ГидроПревентор'
        else:
            # print(pvo_2)
            return pvo_2, f'Монтаж ПВО по схеме №2'



