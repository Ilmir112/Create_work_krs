from datetime import datetime
from openpyxl.styles import Border, Side


class ProtectedIsDigit:
    def __init__(self, default_value=None, name=None):
        self._value = default_value
        self._name = name

    def __get__(self, instance, owner):
        if not instance:
            # print(f'значение {self._name} ра3вно {self._value}')
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if 'уст' in str(value).lower():
            self._value = 0
        elif isinstance(value, str):
            try:
                float_value = float(value.replace(",", "").replace(".", ""))  # Пробуем преобразовать строку в число
                self._value = float_value
            except ValueError:
                self._value = None  # Если не удалось преобразовать в число, сохраняем None
        elif isinstance(value, (int, float)):
            self._value = float(value)  # Преобразуем целое число в число с плавающей точкой
        else:
            print(f'Ошибка: Недопустимое значение {value}')


class ProtectedIsNonNone:
    def __init__(self, default_value=None, name=None):
        self._value = default_value
        self._name = name

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value is not None and not str(value).replace(",", "").replace(".", "").isdigit():
            instance.__dict__[self._name] = value

        else:
            print(f'Ошибка: {value} - не корректное строковое значение')
            raise ValueError("Значение должно быть строкой")


well_area = ProtectedIsNonNone('не корректно')
well_number = ProtectedIsNonNone('не корректно')
inv_number = ProtectedIsNonNone('не корректно')
cdng = ProtectedIsNonNone('не корректно')

bottomhole_drill = ProtectedIsNonNone('не корректно')
bottomhole_artificial = ProtectedIsNonNone('не корректно')
max_angle = ProtectedIsNonNone('не корректно')
max_angle_H = ProtectedIsNonNone('не корректно')
stol_rotora = ProtectedIsNonNone('не корректно')
column_conductor_diametr = ProtectedIsNonNone('не корректно')
column_conductor_wall_thickness = ProtectedIsNonNone('не корректно')
column_conductor_lenght = ProtectedIsNonNone('не корректно')
level_cement_direction = ProtectedIsNonNone('не корректно')
level_cement_conductor = ProtectedIsNonNone('не корректно')
column_diametr = ProtectedIsNonNone('не корректно')
column_wall_thickness = ProtectedIsNonNone('не корректно')
shoe_column = ProtectedIsNonNone('не корректно')
level_cement_column = ProtectedIsNonNone('не корректно')
pressuar_mkp = ProtectedIsNonNone('не корректно')
column_additional_diametr = ProtectedIsNonNone('не корректно')
column_additional_wall_thickness = ProtectedIsNonNone('не корректно')
head_column_additional = ProtectedIsNonNone('не корректно')
shoe_column_additional = ProtectedIsNonNone('не корректно')
column_direction_lenght = ProtectedIsDigit('не корректно')

column_direction_diametr = ProtectedIsNonNone('не корректно')
column_direction_wall_thickness = ProtectedIsNonNone('не корректно')

problemWithEk_diametr = 220
cdng = ProtectedIsNonNone('не корректно')
data_fond_min = ProtectedIsDigit(0)
cat_well_min = ProtectedIsDigit(0)
cat_well_max = ProtectedIsDigit(0)
data_well_max = ProtectedIsDigit(0)
data_pvr_max = ProtectedIsDigit(0)
q_water = ProtectedIsDigit(0)
proc_water = ProtectedIsDigit(100)
data_well_min = ProtectedIsDigit(0)
data_pvr_min = ProtectedIsDigit(0)
pipes_ind = ProtectedIsDigit(0)
condition_of_wells = ProtectedIsDigit(0)
static_level = ProtectedIsNonNone('не корректно')
dinamic_level = ProtectedIsNonNone('не корректно')
sucker_rod_ind = ProtectedIsDigit(0)
data_x_max = ProtectedIsDigit(0)
data_x_min = ProtectedIsDigit(0)

problemWithEk = False
plast_all = {}
konte_true = False
gipsInWell = False
grp_plan = False
nktOpressTrue = False
open_trunk_well = False
lift_ecn_can = False
pause = True
curator = '0'
lift_ecn_can_addition = False
column_passability = False
column_additional_passability = False
column_direction_True = False
work_perforations_approved = False
leakiness = False
emergency_well = False
column_additional = False
without_damping = False
well_number = None
well_area = None
bvo = False
old_version = True
skm_depth = 0
pakerTwoSKO = False
normOfTime = 0
Qoil = 0
template_depth = 0
nkt_diam = 73
b_plan = 0
expected_Q = 0
expected_P = 0
plast_select = ''
dict_perforation = {}
dict_perforation_project = {}
itog_ind_min = 0
work_plan = None
kat_pvo = 2
gaz_f_pr = []
paker_diametr = 0
cat_gaz_f_pr = []
paker_layout = 0
column_diametr = 0
column_wall_thickness = 0
shoe_column = 0
bottomhole_artificial = 0
max_expected_pressure = 0
leakiness_Count = 0

expected_pick_up = {}
current_bottom = 0
fluid_work = 0
static_level = 0
dinamic_level = 0
ins_ind = 0
number_dp = ''
len_razdel_1 = 0
current_bottom = 0
count_template = 0

dict_leakiness = {}
dict_perforation_short = {}

emergency_count = 0
skm_interval = []
work_perforations = []
work_perforations_dict = {}
paker_do = {"do": 0, "posle": 0}
values = []
depth_fond_paker_do = {"do": 0, "posle": 0}
paker2_do = {"do": 0, "posle": 0}
depth_fond_paker2_do = {"do": 0, "posle": 0}
perforation_roof = 50000
perforation_sole = 0
dict_pump_SHGN = {"do": '0', "posle": '0'}
dict_pump_ECN = {"do": '0', "posle": '0'}
dict_pump_SHGN_h = {"do": '0', "posle": '0'}
dict_pump_ECN_h = {"do": '0', "posle": '0'}
dict_pump = {"do": '0', "posle": '0'}
leakiness_interval = []
dict_pump_h = {"do": 0, "posle": 0}

well_volume_in_PZ = []
cat_P_1 = []
costumer = 'ОАО "Башнефть"'
contractor = 'ООО "Ойл-Сервис'
dict_contractor = {'ООО "Ойл-Сервис':
    {
        'Дата ПВО': '15.10.2021г'
    }
}
countAcid = 0
swabTypeComboIndex = 1
swab_true_edit_type = 1

drilling_interval = []
max_angle = 0

privyazkaSKO = 0
nkt_mistake = False
H2S_pr = []
cat_H2S_list = []
H2S_mg = []
H2S_mg_m3 = []
lift_key = 0
dict_category = {}
max_admissible_pressure = 0
region = ''
dict_nkt = {}
dict_nkt_po = {}

dict_sucker_rod = {}
dict_sucker_rod_po = {}
row_expected = []
rowHeights = []
plast_project = []
plast_work = []
leakage_window = None
cat_P_P = []
well_oilfield = 0
template_depth_addition = 0
nkt_template = 59

well_volume_in_PZ = []
image_list = []
problemWithEk_depth = 10000
thin_border = Border(left=Side(style='thin'),
                     right=Side(style='thin'),
                     top=Side(style='thin'),
                     bottom=Side(style='thin'))


def if_None(value):
    if isinstance(value, datetime):
        return value
    elif value is None or 'отс' in str(value).lower() or str(value).replace(' ', '') == '-' \
            or value == 0 or str(value).replace(' ', '') == '':
        return 'отсут'
    else:
        return value
