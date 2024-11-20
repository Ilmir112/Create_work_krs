import math
from abc import ABC, abstractmethod


class VolumeWell(ABC):
    @abstractmethod
    def volume_well_calculate(self):
        pass

    def area_calculate(self, column_diametr, column_wall_thickness):
        return ((column_diametr - 2 * column_wall_thickness) / 1000) ** 2 * math.pi / 4

    @abstractmethod
    def volume_well_pod_nkt(self):
        pass

    @abstractmethod
    def volume_calculate_roof_of_sole(self, roof, sole):
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
                        FindIndexPZ.check_str_none(None, diam_rod) / 1000) / lenght_rod) ** 2) / 4 * lenght_rod
        return round(volume_rod, 5)


class VolumeWellWithoutExstraColumn(VolumeWell):
    def __init__(self, dict_data_well):
        self.dict_data_well = dict_data_well
        self.column_diametr = dict_data_well["column_diametr"]._value
        self.column_wall_thickness = dict_data_well["column_wall_thickness"]._value
        self.current_bottom = dict_data_well["current_bottom"]
        self.area_column = self.area_calculate(self.column_diametr, self.column_wall_thickness)
        if self.dict_data_well["head_column"]._value != 0:
            self.area_well_without_column = self.area_calculate(self.dict_data_well["diametr_doloto_ek"]._value, 0)

    def volume_well_calculate(self):
        return round(self.area_column * self.current_bottom, 1)

    def volume_well_pod_nkt(self):
        nkt_lenght = round(sum(list(self.dict_data_well["dict_nkt"].values())), 1)
        volume_well_pod_nkt = self.area_column * (
                float(self.dict_data_well["current_bottom"]) - float(nkt_lenght))
        return round(volume_well_pod_nkt, 1)

    def volume_calculate_roof_of_sole(self, roof, sole):

        if self.dict_data_well["head_column"]._value == 0:
            return round(self.area_column * (sole - roof))
        else:
            if float(sole) > self.dict_data_well["head_column"]._value and float(roof) > self.dict_data_well["head_column"]._value:
                return round(self.area_column * (sole - roof), 1)
            elif float(sole) < self.dict_data_well["head_column"]._value and float(roof) < self.dict_data_well["head_column"]._value:
                return round(self.area_well_without_column * (sole - roof), 1)
            else:
                return round(self.area_column * (
                        sole - float(self.dict_data_well["head_column"]._value)) + \
                       self.area_well_without_column * (float(self.dict_data_well["head_column"]._value) - roof), 1)


class VolumeWellWithExstraColumn(VolumeWell):
    def __init__(self, dict_data_well):
        self.dict_data_well = dict_data_well

        self.column_diametr = dict_data_well["column_diametr"]._value
        self.column_wall_thickness = dict_data_well["column_wall_thickness"]._value
        self.column_diametr_additional = dict_data_well["column_additional_diametr"]._value
        self.column_wall_thickness_additional = dict_data_well["column_additional_wall_thickness"]._value
        self.current_bottom = dict_data_well["current_bottom"]

        self.head_column_additional = dict_data_well["head_column_additional"]._value
        self.area_column = self.area_calculate(self.column_diametr, self.column_wall_thickness)
        self.area_column_additional = self.area_calculate(self.column_diametr_additional,
                                                          self.column_wall_thickness_additional)
        if self.dict_data_well["head_column"]._value != 0:
            self.area_well_without_column = self.area_calculate(self.dict_data_well["diametr_doloto_ek"], 0)

    def volume_well_calculate(self):
        return round(self.area_column * self.head_column_additional +
                     self.area_column_additional *
                     (self.head_column_additional - self.current_bottom), 1)

    def volume_well_pod_nkt(self):
        nkt_lenght = round(sum(list(self.dict_data_well["dict_nkt"].values())), 1)
        if (round(sum(list(self.dict_data_well["dict_nkt"].values())), 1) >
                float(self.dict_data_well["head_column_additional"]._value)):
            volume_well_pod_nkt = self.area_column_additional * (
                    float(self.dict_data_well["current_bottom"] - int(nkt_lenght)) / 1000)
        else:
            volume_well_pod_nkt = self.area_column * (
                    float(self.dict_data_well["current_bottom"]) - int(nkt_lenght)) / 1000
        return round(volume_well_pod_nkt, 1)

    def volume_calculate_roof_of_sole(self, roof, sole):
        if self.dict_data_well["head_column"]._value == 0:
            if sole and roof > float(self.dict_data_well["head_column_additional"]._value):
                return round(self.area_column_additional * (sole - roof))
            elif sole and roof < float(self.dict_data_well["head_column_additional"]._value):
                return round(self.area_column * (sole - roof))
            else:
                return round(self.area_column_additional * (
                            sole - float(self.dict_data_well["head_column_additional"]._value))) + \
                       self.area_column * (float(self.dict_data_well["head_column_additional"]._value) - roof)
        else:
            if sole and roof > self.dict_data_well["head_column"]._value:
                return round(self.area_column * (sole - roof))
            elif sole and roof < self.dict_data_well["head_column"]._value:
                return round(self.area_well_without_column * (sole - roof))
            else:
                return round(self.area_well_without_column * (
                        sole - float(self.dict_data_well["head_column"]._value))) + \
                       self.area_column * (float(self.dict_data_well["head_column"]._value) - roof)


def volume_work(dict_data_well):
    if dict_data_well["column_additional"] is False or (dict_data_well["column_additional"] and
                                                        dict_data_well["head_column_additional"]._value >=
                                                        dict_data_well["current_bottom"]):
        volume_well = VolumeWellWithoutExstraColumn(dict_data_well)
        return volume_well.volume_well_calculate()
    else:
        volume_well = VolumeWellWithExstraColumn(dict_data_well)
        return volume_well.volume_well_calculate()


def volume_calculate_roof_of_sole(dict_data_well, roof, sole):
    roof = float(roof)
    sole = float(sole)
    if dict_data_well["column_additional"] is False or (dict_data_well["column_additional"] and
                                                        dict_data_well["head_column_additional"]._value >=
                                                        sole):
        volume_well = VolumeWellWithoutExstraColumn(dict_data_well)
        return volume_well.volume_calculate_roof_of_sole(roof, sole)
    else:
        volume_well = VolumeWellWithExstraColumn(dict_data_well)
        return volume_well.volume_calculate_roof_of_sole(roof, sole)


def volume_well_pod_nkt_calculate(
        dict_data_well):  # Расчет необходимого объема внутри НКТ и между башмаком НКТ и забоем

    if (dict_data_well["column_additional"] is False or
            (dict_data_well["column_additional"] and
             dict_data_well["head_column_additional"]._value >= dict_data_well["current_bottom"])):
        volume_well = VolumeWellWithoutExstraColumn(dict_data_well)
        return volume_well.volume_well_pod_nkt()

    elif round(sum(list(dict_data_well["dict_nkt"].values())), 1) > float(
            dict_data_well["head_column_additional"]._value):
        volume_well = VolumeWellWithExstraColumn(dict_data_well)

        return volume_well.volume_well_pod_nkt()


def volume_jamming_well(dict_data_well):  # объем глушения скважины

    volume_jamming_well = round(
        (volume_work(dict_data_well) - volume_nkt_metal(dict_data_well) - volume_rod(dict_data_well)) * 1.1,
        1)
    return volume_jamming_well


def volume_rod(dict_data_well):  # Объем штанг

    from find import FindIndexPZ
    volume_rod = 0
    # print(dict_sucker_rod)
    if "sucker_rod" in list(dict_data_well.keys()):
        for diam_rod, lenght_rod in dict_data_well["sucker_rod"].items():
            if diam_rod:
                volume_rod += (3.14 * (lenght_rod * (
                        FindIndexPZ.check_str_none(None, diam_rod) / 1000) / lenght_rod) ** 2) / 4 * lenght_rod
    return round(volume_rod, 5)


def volume_nkt_metal(dict_data_well):  # Внутренний объем НКТ железа по фондовым
    volume_nkt_metal = 0
    for nkt, length_nkt in dict_data_well["dict_nkt"].items():
        if '73' in str(nkt):
            volume_nkt_metal += 1.17 * length_nkt / 1000
        elif '60' in str(nkt):
            volume_nkt_metal += 0.87 * length_nkt / 1000
        elif '89' in str(nkt):
            volume_nkt_metal += 1.7 * length_nkt / 1000
        elif '48' in str(nkt):
            volume_nkt_metal += 0.55 * length_nkt / 1000
    return round(volume_nkt_metal, 1)


def volume_nkt(dict_data_well):  # Внутренний объем НКТ по фондовым НКТ
    volume_nkt = 0

    if "dict_nkt" in list(dict_data_well.keys()):
        for nkt, length_nkt in dict_data_well["dict_nkt"].items():
            if nkt:
                volume_nkt += (float(nkt) - 2 * 7.6) ** 2 * 3.14 / 4 / 1000000 * length_nkt
    # print(f'объем НКТ {volume_nkt}')
    return round(volume_nkt, 1)
