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


column_head_m = ''
date_drilling_cancel = ''
date_drilling_run = ''
wellhead_fittings = ''
well_area = ProtectedIsNonNone('не корректно')
well_number = ProtectedIsNonNone('не корректно')
inv_number = ProtectedIsNonNone('не корректно')
cdng = ProtectedIsNonNone('не корректно')
gnkt_number = 0
gnkt_length = 0
diametr_length = 0
emergency_bottom = ''
iznos = 0
pipe_mileage = 0
pipe_fatigue = 0
pvo = 0
previous_well = 0
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
index_row_pvr_list = []
gis_list = []
pvr_row = []
current_date = datetime.now().date()
pressuar_mkp = ProtectedIsNonNone('не корректно')
column_additional_diametr = ProtectedIsNonNone('не корректно')
column_additional_wall_thickness = ProtectedIsNonNone('не корректно')
head_column_additional = ProtectedIsNonNone('не корректно')
shoe_column_additional = ProtectedIsNonNone('не корректно')
column_direction_lenght = ProtectedIsDigit('не корректно')

column_direction_diametr = ProtectedIsNonNone('не корректно')
column_direction_wall_thickness = ProtectedIsNonNone('не корректно')
data_list = []
problemWithEk_diametr = 220
cdng = ProtectedIsNonNone('не корректно')
data_fond_min = ProtectedIsDigit(0)
cat_well_min = ProtectedIsDigit(0)
cat_well_max = ProtectedIsDigit(0)
data_well_max = ProtectedIsDigit(0)
first_pressure = ProtectedIsDigit(0)
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
plast_all = []
konte_true = False
gipsInWell = False
grp_plan = False
nktOpressTrue = False
open_trunk_well = False
lift_ecn_can = False
sucker_rod_none = True
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
angle_data = []
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
# host_krs = '31.129.99.186'
host_krs = '176.109.106.199'
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

ins_ind = 0
number_dp = 0
len_razdel_1 = 0
current_bottom = 0
count_template = 0
forPaker_list = False
current_bottom2 = 5000
dict_leakiness = {}
dict_perforation_short = {}

emergency_count = 0
skm_interval = []
category_pressuar = 3
category_h2s = 3
category_gf = 3
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
h2s_pr = []
cat_h2s_list = []
h2s_mg = []
h2s_mg_m3 = []
lift_key = 0
dict_category = {}
max_admissible_pressure = 0
region = ''
data_in_base = False
dict_nkt = {}
dict_nkt_po = {}
path_image = '_internal/'
# path_image = ''
data_well_dict = {}
Qwater = 100
dict_sucker_rod = {}
dict_sucker_rod_po = {}
row_expected = []
rowHeights = []
plast_project = []
plast_work = []
leakage_window = None
cat_P_P = []
data_well_is_True = False
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
postgres_params_classif = {
            f'database': 'databaseclassification',
            f'user': 'postgres',
            f'password': '195375AsD+',
            f'host': f'{host_krs}',
            f'port': '5432'
        }
postgres_params_data_well = {
            f'database': 'well_data',
            f'user': 'postgres',
            f'password': '195375AsD+',
            f'host': f'{host_krs}',
            f'port': '5432'
        }

postgres_conn_gnkt = {
    'database': 'gnkt_database',
    'user': 'postgres',
    'password': '195375AsD+',
    f'host': f'{host_krs}',
    'port': '5432'
        }
postgres_conn_work_well = {
    'database': 'databasewellwork',
    'user': 'postgres',
    'password': '195375AsD+',
    f'host': f'{host_krs}',
    'port': '5432'
}
postgres_conn_user = {
    'database': 'krs2',
    'user': 'postgres',
    'password': '195375AsD+',
    f'host': f'{host_krs}',
    'port': '5432'
}

dict_telephon = {'Бригада № 1': 9228432791,
                 'Бригада № 2': 9174006602,
                 'Бригада № 3': 9174009883,
                 'Бригада № 4': 9228035896,
                 'Бригада № 5': 9228432597,
                 'Бригада № 7 ': 9228451907,
                 'Бригада № 8': 9228452018,
                 'Бригада № 9': 9228449698,
                 'Бригада № 10': 9228432980,
                 'Бригада № 12': 9228180254,
                 'Бригада № 14': 9228034462,
                 'Бригада № 15': 9228382609,
                 'Бригада № 16': 9325425972,
                 'Бригада № 17': 9228035385,
                 'Бригада № 18': 9228449048,
                 'Бригада № 19': 9328486359,
                 'Бригада № 20': 9228556638,
                 'Бригада № 21': 9374978836,
                 'Бригада № 22': 9270869338,
                 'Бригада № 23': 9373146981,
                 'Бригада № 24': 9373146135,
                 'Бригада № 25': 9373521496,
                 'Бригада № 28': 9373519867,
                 'Бригада № 29': 9373519358,
                 'Бригада № 30': 9373518753,
                 'Бригада № 31': 9374861861,
                 'Бригада № 33': 9273029571,
                 'Бригада № 34': 9378367419,
                 'Бригада № 36 ': 9374993472,
                 'Бригада № 37': 9273211829,
                 'Бригада № 38': 9273211926,
                 'Бригада № 43': 9273254843,
                 'Бригада № 44': 9273254834,
                 'Бригада № 45': 9273254830,
                 'Бригада № 46': 9373362319,
                 'Бригада № 47': 9373519738,
                 'Бригада № 48': 9378367421,
                 'Бригада № 49': 9378309337,
                 'Бригада № 54': 9270869358,
                 'Бригада № 55': 9279368415,
                 'Бригада № 56': 9279368421,
                 'Бригада № 58': 9270864957,
                 'Бригада № 59': 9174002382,
                 'Бригада № 60 ': 9273460812,
                 'Бригада № 61': 9273029274,
                 'Бригада № 64': 9378452378,
                 'Бригада № 65': 9273029526,
                 'Бригада № 66': 9279368446,
                 'Бригада № 68': 9279368423,
                 'Бригада № 70': 9373084741,
                 'Бригада № 71': 9373085348,
                 'Бригада № 72': 9373085351,
                 'Бригада № 73': 9373310474,
                 'Бригада № 74': 9373639774,
                 'Бригада № 75': 9174009934,
                 'Бригада № 77': 9373639370,
                 'Бригада № 78': 9174001660,
                 'Бригада № 79': 9174003079,
                 'Бригада № 80': 9174002580,
                 'Бригада № 81': 9174003114,
                 'Бригада № 82': 9174002682,
                 'Бригада № 83': 9174001783,
                 'Бригада № 84': 9174002844,
                 'Бригада № 85': 9174001915,
                 'Бригада № 86': 9174002824,
                 'Бригада № 87': 9174002873,
                 'Бригада № 88': 9174002564,
                 'Бригада № 90': 9174002494,
                 'Бригада № 91': 9174002791,
                 'Бригада № 92': 9174008192,
                 'Бригада № 93': 9174002893,
                 'Бригада № 94': 9174002382,
                 'Бригада № 95': 9174009557,
                 'Бригада № 97': 9174008597,
                 'Бригада № 98': 9226245380,
                 'Бригада № 99': 9228739012,
                 'Бригада № 100': 9228390349,
                 'Бригада № 101': 9226245342,
                 'Бригада № 102': 9228180653,
                 'Бригада № 103': 9325425834,
                 'Бригада № 104': 9325559708,
                 'Бригада № 105': 9325300276,
                 'Бригада № 106': 9228378241,
                 'Бригада № 107': 9228377310,
                 'Бригада № 108': 9328425178,
                 'Бригада № 109': 9228378610,
                 'Бригада № 110': 9328489427,
                 'Бригада № 111': 9174002633,
                 'Бригада № 112': 9174006899,
                 'Бригада № 114': 9174002769,
                 'Бригада № 116': 9174009979,
                 'Бригада № 117': 9174001627,
                 'Бригада № 118': 9198625311,
                 'Бригада № 119': 9174002340,
                 'Бригада № 120': 9325426037,
                 'Бригада № 121': 9198625269,
                 'Бригада № 122': 9198625364,
                 'Бригада № 123': 9867803956,
                 'Бригада № 124': 9867804254,
                 'Бригада № 125': 9867806579,
                 'Бригада № 126': 9867807081,
                 'Бригада № 127': 9174007527,
                 'Бригада № 128': 9174002881,
                 'Бригада № 129': 9174002707,
                 'Бригада № 130': 9174001962,
                 'Бригада № 131': 9174001882,
                 'Бригада № 132': 9174009853,
                 'Бригада № 133': 9174002035,
                 'Бригада № 134': 9174009821,
                 'Бригада № 136': 9273211908,
                 'Бригада № 137': 9273460185,
                 'Бригада № 138': 9174008389,
                 'Бригада № 139': 9174003046,
                 'Бригада № 140': 9174003936,
                 'Бригада № 141': 9228378408,
                 'Бригада ТРС № 1': 9228928015,
                 'Бригада ТРС № 2': 9228927913,
                 'Бригада ТРС № 3': 9228928016,
                 'Бригада ГНКТ №1': 9174003142,
                 'Бригада ГНКТ №2': 9174001690}


def if_None(value):
    if isinstance(value, datetime):
        return value
    elif value is None or 'отс' in str(value).lower() or str(value).replace(' ', '') == '-' \
            or value == 0 or str(value).replace(' ', '') == '':
        return 'отсут'
    else:
        return value
