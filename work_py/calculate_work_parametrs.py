import math
from abc import ABC, abstractmethod


class VolumeWell(ABC):
    @abstractmethod
    def volume_well_calculate(self):
        pass

    def area_calculate(self, column_diametr, column_wall_thickness):
        return ((column_diametr - 2 * column_wall_thickness)/1000)**2 * math.pi /4

class VolumeWellWithoutExstraColumn(VolumeWell):
    def __init__(self, column_diametr, column_wall_thickness, current_bottom):
        self.column_diametr = column_diametr
        self.column_wall_thickness = column_wall_thickness
        self.current_bottom = current_bottom

    def volume_well_calculate(self):
        self.area_column = self.area_calculate(self.column_diametr, self.column_wall_thickness)
        return round(self.area_column * self.current_bottom, 1)

class VolumeWellWithExstraColumn(VolumeWell):
    def __init__(self, column_diametr, column_wall_thickness,current_bottom,
                 head_column_additional=0, column_diametr_additional=0, column_wall_thickness_additional=0):
        self.column_diametr = column_diametr
        self.column_wall_thickness = column_wall_thickness
        self.column_diametr_additional = column_diametr_additional
        self.column_wall_thickness_additional = column_wall_thickness_additional
        self.current_bottom = current_bottom

        self.current_bottom = current_bottom
        self.head_column_additional = head_column_additional

    def volume_well_calculate(self):
        self.area_column = self.area_calculate(self.column_diametr, self.column_wall_thickness)
        self.area_column_additional = self.area_calculate(self.column_diametr_additional, self.column_wall_thickness_additional)

        return round(self.area_column * self.head_column_additional +
                     self.area_column_additional *
                     (self.head_column_additional - self.current_bottom), 1)



def volume_work(column_diametr, column_wall_thickness, current_bottom, head_column_additional=0,
              column_diametr_additional=0, column_wall_thickness_additional=0):
    if int(head_column_additional) == 0 or head_column_additional >= current_bottom:
        volume_well = VolumeWellWithoutExstraColumn(column_diametr, column_wall_thickness, current_bottom)
        return volume_well.volume_well_calculate()
    else:
        volume_well = VolumeWellWithExstraColumn(column_diametr, column_wall_thickness, current_bottom,
                 head_column_additional, column_diametr_additional, column_wall_thickness_additional)
        return volume_well.volume_well_calculate()

