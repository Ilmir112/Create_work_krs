from PyQt5.QtWidgets import QInputDialog, QMessageBox


class CalcFond:

    def __init__(self, static_level, len_nkt, fluid, pressuar_nkt, distance_between_nkt):
        self.static_level = static_level
        self.len_nkt = len_nkt
        self.fluid = fluid
        self.pressuar_nkt = pressuar_nkt
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

    def calc_pressuar_list(self):
        pressuar_nkt = self.pressuar_nkt
        calc_nkt_list = self.calc_nkt_dict()
        calc_pressuar_dict = {}
        try:
            for nkt_l in calc_nkt_list:
                if nkt_l <= float(self.static_level):
                    a = self.fluid
                    p = round(float(str(self.fluid)[:3]) * 9.81 * nkt_l / 100, 0)
                else:
                    p = round(float(str(self.fluid)[:3]) * 9.81 * nkt_l / 100-
                              ((nkt_l - float(self.static_level)) * 9.81 * float(str(self.fluid)[:3])) / 100, 0)

                if p >= 150:
                    p = 150

                calc_pressuar_dict[nkt_l] = 149 - p if pressuar_nkt < 149 - p else pressuar_nkt
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка', f'Ошибка расчета опрессовки НКТ {type(e).__name__}\n\n{str(e)}')
        return calc_pressuar_dict

