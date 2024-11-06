import math
from abc import ABC, abstractmethod


class VolumeWell(ABC):
    @abstractmethod
    def volume_well_calculate(self):
        pass

    def area_calculate(self, column_diametr, column_wall_thickness):
        return ((column_diametr - 2 * column_wall_thickness)/1000)**2 * math.pi /4
    @abstractmethod
    def volume_well_pod_nkt(self):
        pass
    @staticmethod
    def volume_nkt_metal(dict_nkt):  # Внутренний объем НКТ железа по фондовым
        volume_nkt_metal = 0
        for nkt, length_nkt in dict_nkt.items():
            if '73' in str(nkt):
                volume_nkt_metal += 1.17 * length_nkt / 1000
            elif '60' in str(nkt):
                volume_nkt_metal += 0.87 * length_nkt / 1000
            elif '89' in str(nkt):
                volume_nkt_metal += 1.7 * length_nkt / 1000
            elif '48' in str(nkt):
                volume_nkt_metal += 0.55 * length_nkt / 1000
        return round(volume_nkt_metal, 1)

    @staticmethod
    def volume_rod(dict_sucker_rod):  # Объем штанг

        from find import FindIndexPZ
        volume_rod = 0
        # print(dict_sucker_rod)
        for diam_rod, lenght_rod in dict_sucker_rod.items():
            if diam_rod:
                volume_rod += (3.14 * (lenght_rod * (
                        FindIndexPZ.check_str_None(None, diam_rod) / 1000) / lenght_rod) ** 2) / 4 * lenght_rod
        return round(volume_rod, 5)



class VolumeWellWithoutExstraColumn(VolumeWell):
    def __init__(self, data_well):
        self.column_diametr = data_well.column_diametr._value
        self.column_wall_thickness = data_well.column_wall_thickness._value
        self.current_bottom = data_well.current_bottom

    def volume_well_calculate(self):
        self.area_column = self.area_calculate(self.column_diametr, self.column_wall_thickness)
        return round(self.area_column * self.current_bottom, 1)

    def volume_well_pod_nkt(self):
        nkt_lenght = round(sum(list(self.data_well.dict_nkt.values())), 1)
        volume_well_pod_nkt = self.area_column * (
                    float(self.data_well.current_bottom) - int(nkt_lenght)) / 1000
        return volume_well_pod_nkt

class VolumeWellWithExstraColumn(VolumeWell):
    def __init__(self, data_well):
        self.data_well = data_well

        self.column_diametr = data_well.column_diametr._value
        self.column_wall_thickness = data_well.column_wall_thickness._value
        self.column_diametr_additional = data_well.column_additional_diametr._value
        self.column_wall_thickness_additional = data_well.column_additional_wall_thickness._value
        self.current_bottom = data_well.current_bottom
        self.head_column_additional = data_well.head_column_additional._value
        self.area_column = self.area_calculate(self.column_diametr, self.column_wall_thickness)
        self.area_column_additional = self.area_calculate(self.column_diametr_additional,
                                                          self.column_wall_thickness_additional)

    def volume_well_calculate(self):


        return round(self.area_column * self.head_column_additional +
                     self.area_column_additional *
                     (self.head_column_additional - self.current_bottom), 1)

    def volume_well_pod_nkt(self):
        nkt_lenght = round(sum(list(self.data_well.dict_nkt.values())), 1)
        if round(sum(list(self.data_well.dict_nkt.values())), 1) > float(self.data_well.head_column_additional._value):
            volume_well_pod_nkt = self. area_column_additional* (
                                float(self.data_well.current_bottom) - int(nkt_lenght)) / 1000
        else:
            volume_well_pod_nkt = self.area_column * (
                    float(self.data_well.current_bottom) - int(nkt_lenght)) / 1000
        return volume_well_pod_nkt






def volume_work(data_well):
    if data_well.column_additional is False or (data_well.column_additional and
                                                data_well.head_column_additional._value >= data_well.current_bottom):
        volume_well = VolumeWellWithoutExstraColumn(data_well)
        return volume_well
    else:
        volume_well = VolumeWellWithExstraColumn(data_well)
        return volume_well


def volume_well_pod_NKT_calculate(data_well):  # Расчет необходимого объема внутри НКТ и между башмаком НКТ и забоем


    if data_well.column_additional is False:
        volume_well = VolumeWellWithoutExstraColumn(data_well)
        return volume_well.volume_well_pod_nkt()

    elif round(sum(list(data_well.dict_nkt.values())), 1) > float(data_well.head_column_additional._value):
        volume_well = VolumeWellWithExstraColumn(data_well)

        return volume_well.volume_well_pod_nkt()
