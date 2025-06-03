from PyQt5.QtWidgets import QMessageBox

from log_files.log import logger


class CalcFond:

    def __init__(self, static_level, len_nkt, fluid, pressure_nkt, distance_between_nkt):
        self.static_level = static_level
        self.len_nkt = len_nkt
        self.fluid = fluid
        self.pressure_nkt = pressure_nkt
        self.distance_between_nkt = distance_between_nkt

    def calc_nkt_dict(self):
        distance_between_nkt = self.distance_between_nkt
        n = distance_between_nkt
        calc_nkt_list = []
        while n <= self.len_nkt:
            calc_nkt_list.append(n)
            n += distance_between_nkt
        calc_nkt_list.append(self.len_nkt)
        return calc_nkt_list

    def calc_pressure_list(self):
        pressure_nkt = self.pressure_nkt
        calc_nkt_list = self.calc_nkt_dict()
        calc_pressure_dict = {}
        try:
            for nkt_l in calc_nkt_list:
                if nkt_l <= float(self.static_level):

                    p = round(float(str(self.fluid)[:3]) * 9.81 * nkt_l / 100, 0)
                else:
                    p = round(float(str(self.fluid)[:3]) * 9.81 * nkt_l / 100-
                              ((nkt_l - float(self.static_level)) * 9.81 * float(str(self.fluid)[:3])) / 100, 0)

                if p >= 150:
                    p = 150

                calc_pressure_dict[nkt_l] = 149 - p if pressure_nkt < 149 - p else pressure_nkt
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка', f'Ошибка расчета опрессовки НКТ {type(e).__name__}\n\n{str(e)}')
            logger.critical(e)
        return calc_pressure_dict

