import math
from abc import ABC, abstractmethod


class VolumeWell(ABC):
    @abstractmethod
    def volume_well_calculate(self):
        pass

    def area_calculate(self, column_diameter, column_wall_thickness):
        return ((column_diameter - 2 * column_wall_thickness) / 1000) ** 2 * math.pi / 4

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
        for diam_rod, length_rod in dict_sucker_rod.items():
            if diam_rod:
                volume_rod += (3.14 * (length_rod * (
                        FindIndexPZ.check_str_none(None, diam_rod) / 1000) / length_rod) ** 2) / 4 * length_rod
        return round(volume_rod, 5)


class VolumeWellWithoutExstraColumn(VolumeWell):
    def __init__(self, data_well):
        self.data_well = data_well
        self.column_diameter = data_well.column_diameter.get_value
        self.column_wall_thickness = data_well.column_wall_thickness.get_value
        self.current_bottom = data_well.current_bottom
        self.area_column = self.area_calculate(self.column_diameter, self.column_wall_thickness)
        if self.data_well.head_column.get_value != 0:
            self.area_well_without_column = self.area_calculate(self.data_well.diameter_doloto_ek.get_value, 0)

    def volume_well_calculate(self):
        return round(self.area_column * self.current_bottom, 1)

    def volume_well_pod_nkt(self):
        nkt_length = round(sum(list(self.data_well.dict_nkt_before.values())), 1)
        volume_well_pod_nkt = self.area_column * (
                float(self.data_well.current_bottom) - float(nkt_length))
        return round(volume_well_pod_nkt, 1)

    def volume_calculate_roof_of_sole(self, roof, sole):

        if self.data_well.head_column.get_value == 0:
            return round(self.area_column * (sole - roof), 1)
        else:
            if float(sole) > self.data_well.head_column.get_value and float(roof) > self.data_well.head_column.get_value:
                return round(self.area_column * (sole - roof), 1)
            elif float(sole) < self.data_well.head_column.get_value and float(roof) < self.data_well.head_column.get_value:
                return round(self.area_well_without_column * (sole - roof), 1)
            else:
                return round(self.area_column * (
                        sole - float(self.data_well.head_column.get_value)) + \
                       self.area_well_without_column * (float(self.data_well.head_column.get_value) - roof), 1)


class VolumeWellWithExstraColumn(VolumeWell):
    def __init__(self, data_well):
        self.data_well = data_well

        self.column_diameter = data_well.column_diameter.get_value
        self.column_wall_thickness = data_well.column_wall_thickness.get_value
        self.column_diameter_additional = data_well.column_additional_diameter.get_value
        self.column_wall_thickness_additional = data_well.column_additional_wall_thickness.get_value
        self.current_bottom = data_well.current_bottom

        self.head_column_additional = data_well.head_column_additional.get_value
        self.area_column = self.area_calculate(self.column_diameter, self.column_wall_thickness)
        self.area_column_additional = self.area_calculate(self.column_diameter_additional,
                                                          self.column_wall_thickness_additional)
        if self.data_well.head_column.get_value != 0:
            self.area_well_without_column = self.area_calculate(self.data_well.diameter_doloto_ek, 0)

    def volume_well_calculate(self):
        return round(self.area_column * self.head_column_additional +
                     self.area_column_additional *
                     (self.head_column_additional - self.current_bottom), 1)

    def volume_well_pod_nkt(self):
        nkt_length = round(sum(list(self.data_well.dict_nkt_before.values())), 1)
        if nkt_length > float(self.data_well.head_column_additional.get_value):
            volume_well_pod_nkt = self.area_column_additional * (
                    float(self.data_well.current_bottom - int(nkt_length)))
        else:
            volume_add = self.area_column_additional * (
                    float(self.data_well.current_bottom) - int(nkt_length))
            volume_ek = self.area_column * (float(self.data_well.head_column_additional.get_value - nkt_length))

            volume_well_pod_nkt = round(volume_add + volume_ek, 1)

        return volume_well_pod_nkt

    def volume_calculate_roof_of_sole(self, roof, sole):
        if self.data_well.head_column.get_value == 0:
            if sole and roof > float(self.data_well.head_column_additional.get_value):
                return round(self.area_column_additional * (sole - roof))
            elif sole and roof < float(self.data_well.head_column_additional.get_value):
                return round(self.area_column * (sole - roof))
            else:
                return round(self.area_column_additional * (
                            sole - float(self.data_well.head_column_additional.get_value))) + \
                       self.area_column * (float(self.data_well.head_column_additional.get_value) - roof)
        else:
            if sole and roof > self.data_well.head_column.get_value:
                return round(self.area_column * (sole - roof))
            elif sole and roof < self.data_well.head_column.get_value:
                return round(self.area_well_without_column * (sole - roof))
            else:
                return round(self.area_well_without_column * (
                        sole - float(self.data_well.head_column.get_value))) + \
                       self.area_column * (float(self.data_well.head_column.get_value) - roof)


def volume_work(data_well):
    if data_well.column_additional is False or (data_well.column_additional and
                                                        data_well.head_column_additional.get_value >=
                                                        data_well.current_bottom):
        volume_well = VolumeWellWithoutExstraColumn(data_well)
        return volume_well.volume_well_calculate()
    else:
        volume_well = VolumeWellWithExstraColumn(data_well)
        return volume_well.volume_well_calculate()


def volume_calculate_roof_of_sole(data_well, roof, sole):
    roof = float(roof)
    sole = float(sole)
    if data_well.column_additional is False or (data_well.column_additional and
                                                        data_well.head_column_additional.get_value >=
                                                        sole):
        volume_well = VolumeWellWithoutExstraColumn(data_well)
        return volume_well.volume_calculate_roof_of_sole(roof, sole)
    else:
        volume_well = VolumeWellWithExstraColumn(data_well)
        return volume_well.volume_calculate_roof_of_sole(roof, sole)


def volume_well_pod_nkt_calculate(
        data_well):  # Расчет необходимого объема внутри НКТ и между башмаком НКТ и забоем

    if (data_well.column_additional is False or
            (data_well.column_additional and
             data_well.head_column_additional.get_value >= data_well.current_bottom)):
        volume_well = VolumeWellWithoutExstraColumn(data_well)
        return volume_well.volume_well_pod_nkt()

    else:
        # round(sum(list(data_well.dict_nkt_before.values())), 1) > float(
        #     data_well.head_column_additional.get_value):
        volume_well = VolumeWellWithExstraColumn(data_well)


        return volume_well.volume_well_pod_nkt()


def volume_jamming_well(data_well):  # объем глушения скважины

    volume_jamming_well = round(
        (volume_work(data_well) - volume_nkt_metal(data_well) - volume_rod(data_well)) * 1.1,
        1)
    return volume_jamming_well


def volume_rod(data_well):  # Объем штанг

    from find import FindIndexPZ
    volume_rod = 0
    # print(dict_sucker_rod)
    if data_well.dict_sucker_rod:
        for diam_rod, length_rod in data_well.dict_sucker_rod.items():
            if diam_rod:
                volume_rod += (3.14 * (length_rod * (
                        FindIndexPZ.check_str_none(None, diam_rod) / 1000) / length_rod) ** 2) / 4 * length_rod
    return round(volume_rod, 5)


def volume_nkt_metal(data_well):  # Внутренний объем НКТ железа по фондовым
    volume_nkt_metal = 0
    for nkt, length_nkt in data_well.dict_nkt_before.items():
        if '73' in str(nkt):
            volume_nkt_metal += 1.17 * length_nkt / 1000
        elif '60' in str(nkt):
            volume_nkt_metal += 0.87 * length_nkt / 1000
        elif '89' in str(nkt):
            volume_nkt_metal += 1.7 * length_nkt / 1000
        elif '48' in str(nkt):
            volume_nkt_metal += 0.55 * length_nkt / 1000
    return round(volume_nkt_metal, 1)


def volume_nkt(data_well):  # Внутренний объем НКТ по фондовым НКТ
    volume_nkt = 0

    if data_well.dict_nkt_before:
        for nkt, length_nkt in data_well.dict_nkt_before.items():
            if nkt:
                if '73' in str(nkt):
                    nkt = 73
                elif '60' in str(nkt):
                    nkt = 60
                elif '89' in str(nkt):
                    nkt = 89
                elif '48' in str(nkt):
                    nkt = 48
                volume_nkt += (float(nkt) - 2 * 7.6) ** 2 * 3.14 / 4 / 1000000 * length_nkt
    # print(f'объем НКТ {volume_nkt}')
    return round(volume_nkt, 1)
