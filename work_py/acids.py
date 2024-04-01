from PyQt5.QtWidgets import QInputDialog, QMessageBox

import krs
import well_data

from .rationingKRS import liftingNKT_norm, descentNKT_norm


def acidGons(self):
    
    plast, ok = QInputDialog.getItem(self, 'выбор пласта для ОПЗ ', 'выберете пласта дл перфорации',
                                     well_data.plast_work, 0, False)
    acid_list = ['HCl', 'HF', 'ВТ', 'Нефтекислотка']
    acid, ok = QInputDialog.getItem(self, 'Вид кислоты', 'Введите вид кислоты:', acid_list, 0, False)
    if ok and acid_list:
        self.le.setText(acid)
    acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
    acid_pr, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
    acid_countOfpoint, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите объем кислоты на точку', 5, 1, 24)
    acid_points, ok = QInputDialog.getText(self, 'точки ГОНС', 'Введите точки ГОНС ')
    bottom_point = max(list(map(int, acid_points.replace('м', '').replace(',', '').split())))
    gons_list = [[f'Спуск гидромониторную насадку до глубины нижней точки до {bottom_point}', None,
     f'Спустить  гидромониторную насадку '
     f'{"".join([f" + НКТ60мм {round(well_data.current_bottom -well_data.head_column_additional._value, 0)}" if well_data.column_additional is True else ""])} '
     f'на НКТ{well_data.nkt_diam}мм до глубины нижней точки до {bottom_point}'
     f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.',
     None, None, None, None, None, None, None,
     'мастер КРС', descentNKT_norm(bottom_point,1)],
     [f' ГОНС пласта {plast} (общий объем {acid_V}м3) в инт. {acid_points}', None,
      f'Провести ОПЗ пласта {plast} силами СК Крезол по технологии ГОНС в инт. {acid_points} с закачкой HCL '
      f'{acid_pr}% в объеме по {acid_countOfpoint}м3/точке (общий объем {acid_V}м3)  в присутствии представителя '
      f'сектора супервайзерского контроля за текущим и капитальным ремонтом скважин (ГОНС произвести снизу-вверх).',
      None, None, None, None, None, None, None,
      'мастер КРС', 8],
     [None, None,
      f'По согласованию с заказчиком  допустить компоновку до глубины {well_data.current_bottom}м, промыть скважину '
      f'прямой промывкой через желобную ёмкость водой у= {well_data.fluid_work} в присутствии представителя заказчика в '
      f'объеме {round(krs.well_volume(self, well_data.current_bottom), 1)}м3. Промывку производить в емкость для дальнейшей утилизации на НШУ с целью недопущения попадания кислоты в систему сбора.',
      None, None, None, None, None, None, None,
      'мастер КРС', 1.2],
     [None, None,
      f'Поднять гидромониторную насадку на НКТ{well_data.nkt_diam}мм c глубины {well_data.current_bottom}м с доливом скважины в '
      f'объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
      None, None, None, None, None, None, None,
      'мастер КРС',
      liftingNKT_norm(well_data.current_bottom, 1)]]
    return gons_list