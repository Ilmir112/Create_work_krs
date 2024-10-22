import math
from abc import ABC, abstractmethod
from well_data import column_diametr, column_additional, column_wall_thickness, current_bottom,\
    head_column_additional, column_additional_diametr, column_additional_wall_thickness


class VolumeWell(ABC):
    def __init__(self):
        super().__init__()

        self.column_diametr, self.column_wall_thickness, self.current_bottom = \
            column_diametr._value, column_wall_thickness._value, current_bottom
        self.column_additional = column_additional
        self.head_column_additional = head_column_additional._value
        self.column_diametr_additional = column_additional_diametr._value
        self.column_wall_thickness_additional = column_additional_wall_thickness._value
    @abstractmethod
    def volume_well_calculate(self):
        pass

    def area_calculate(self):

        return ((self.column_diametr - 2 * self.column_wall_thickness)/1000)**2 * math.pi /4

class VolumeWellWithoutExstraColumn(VolumeWell):
    def __init__(self):
        super().__init__()

    def volume_well_calculate(self):
        self.area_column = self.area_calculate()
        return round(self.area_column * self.current_bottom, 1)

class VolumeWellWithExstraColumn(VolumeWell):
    def __init__(self):
        super().__init__()

    @classmethod
    def volume_well_calculate(cls):
        cls.area_column = cls.area_calculate()
        cls.area_column_additional = cls.area_calculate()

        return round(cls.area_column * cls.head_column_additional +
                     cls.area_column_additional *
                     (cls.head_column_additional - cls.current_bottom), 1)



def volume_work(current_bottom2):


    well_data = VolumeWellWithoutExstraColumn()
    if column_additional == True:
        well_data = VolumeWellWithExstraColumn()
    current_bottom = current_bottom2


    return well_data.volume_well_calculate()

