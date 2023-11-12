import openpyxl as op
from datetime import datetime

from cdng import region_dict, region_p, events_gnvp
import json


def region(cdng):
    region = ''.join([key for key, value in region_dict.items() if cdng in value])
    return region

# выбор подписантов в зависимости от вида ГТМ
def curator_sel(self, curator, region):
    with open('podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)
    if curator == 'ОР':
        return (podpis_dict[region]['ruk_orm']['post'], podpis_dict[region]["ruk_orm"]['surname'])
    elif curator == 'ГТМ':
        return (podpis_dict[region]["ruk_gtm"]['post'], podpis_dict[region]["ruk_gtm"]['surname'])
    elif curator == 'ГО':
        return (podpis_dict[region]['go']['post'], podpis_dict[region]["go"]['surname'])

current_datetime = datetime.today()

# Выбор подписантов в зависимости от региона
def pop_down(self, region, curator_sel):
    from open_pz import CreatePZ
    nach_tkrs_list = ['А.Р.Габдулхаков ', 'З.К. Алиев', 'М.К.Алиев']
    if region == 'ЧГМ' or region == 'ТГМ':
        nach_tkrs = nach_tkrs_list[0]
    elif region == 'КГМ' or region == 'АГМ':
        nach_tkrs = nach_tkrs_list[1]
    elif region == 'ИГМ':
        nach_tkrs = nach_tkrs_list[2]

    with open('podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)

    podp_down = [
        [None, None, None, None, None, None, '"_____"__________________', None, f'{current_datetime.year}г.', None,
         None, None],
        [None, 'План работ составил Ведущий геолог Ойл-сервис', None, None, None, None, None, None, None,
         '/И.М. Зуфаров/', None, None],
        [None, None, None, None, None, None, None, None, None, '     дата подписания', None, None],
        [None, None, 'Начальник ЦТКРС ООО  " Ойл-Сервис"', None, None, None, None, None, None,
         ''.join(nach_tkrs), None, None],
        [None, None, None, None, None, None, None, None, None, '     дата подписания', None, None],
        [None, ' ', 'Согласовано:', None, None, None, None, None, None, None, None, None],

        [None, None, None, None, None, None, '', None, None, '', None, None],
        [None, curator_sel[0], None, None, None, None, '___________________', None, None,
         curator_sel[1], None, None],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, podpis_dict[region]['ruk_pto']['post'], None, None, None, None, None, None, None,
         podpis_dict[region]["ruk_pto"]['surname'], None, ' '],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, podpis_dict[region]['usrs']['post'], None, None, None, None,
         None, None, None, podpis_dict[region]['usrs']['surname'], None, None],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, None, None, None, None, None, None, None, None, None, None, None],

        [None, 'Замечания:', None, None, None, None, None, None, None, None, None, None],
        [None, '1.', '________________________________________________________________________________________________', None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '2.', '________________________________________________________________________________________________', None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '3.', '________________________________________________________________________________________________', None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '4.', '________________________________________________________________________________________________', None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '5.', '________________________________________________________________________________________________', None, None, None, None,
         None,
         None,
         None, None, None],
        [None, None, None, 'Проинструктированы, с планом работ ознакомлены:                         ', None,
         None, None, None, None, None, None, None],
        [None, None, 'Мастер бригады', None, None, None, 'Инструктаж провел мастер бригады ООО "Ойл-Сервис"',
         None, None, None, None, None],
        [None, None, 'Мастер бригады', None, None, None, None, None, None, None, 'подпись', None],
        [None, 'Бурильщик ООО "Ойл-Сервис"', None, None,
         '_____________________Бурильщик ООО "Ойл-Сервис"________________________', None, None, None, None,
         None, None, None],
        [None, 'Пом.бур-ка ООО "Ойл-Сервис"', None, None,
         '_____________________Пом.бур-ка ООО "Ойл-Сервис"_______________________', None, None, None, None,
         None, None, None],
        [None, 'Пом.бур-ка ООО "Ойл-Сервис"', None, None,
         '_____________________Пом.бур-ка ООО "Ойл-Сервис"_______________________', None, None, None, None,
         None, None, None],
        [None, None, 'Машинист', None,
         '_____________________ Машинист                      ________________________', None, None, None,
         None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None]]

    ved_gtm_list = [None, podpis_dict[region]['ved_gtm']['post'], None, None, None, None,  '"___"___________' , None, None, podpis_dict[region]['ved_gtm']['surname'], None, None]

    ved_orm_list = [None, podpis_dict[region]['ved_orm']['post'], None, None, None, None, '"___"___________', None, None, podpis_dict[region]['ved_orm']['surname'], None, None]
    if (region == 'ЧГМ' or region == 'КГМ') and CreatePZ.curator == 'ОР':

        podp_down.insert(13, ved_orm_list)
    elif region == 'КГМ' or region == 'ЧГМ' and CreatePZ.curator == 'ГТМ':
        podp_down.insert(13, ved_gtm_list)
    return podp_down
def razdel_1(self):
    from open_pz import CreatePZ

    with open('podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)

    razdel_1 = [[None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
                [None, podpis_dict[CreatePZ.region]['gi']['post'], None, None, None, None, None,
                  'Главный Инженер ООО "Ойл-Сервис"', None, None, None, None],
                [None, f'____________{podpis_dict[CreatePZ.region]["gi"]["surname"]}', None, None, None, None, None,
                 '_____________А.Р. Хасаншин', None, None, None, None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None,
                 f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, podpis_dict[CreatePZ.region]['gg']['post'], None, None, None,
                 None,
                 None, 'Главный геолог ООО "Ойл-Сервис"', None, None, None, None],
                [None, f'_____________{podpis_dict[CreatePZ.region]["gg"]["surname"]}',None , None, None, None,  None,
                 '_____________Д.Д. Шамигулов', None, None,'',
                 None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, '', None, None,
                 f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None]]

    podp_grp = [[None, 'Представитель подрядчика по ГРП', None, None, None, None, None, None, None, None, None,
                 None],
                [None, '_____________', None, None, None, None, None, None, None, None, None, None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
                 None, None, None,
                 None]]
    podp_bvo =  [
                [None, 'Районный инженер Башкирского ', None, None, None, None, None, None, None, None, None, None],
                [None, 'военизированного отряда ', None, None, None, None, None, None, None, None, None, None],
                [None, '_____________', None, None, None, None, None, None, None, None, None, None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
                 None, None, None,
                 None]]

    if '1' in CreatePZ.cat_P_1 or '1' in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_P_1 or 1 in CreatePZ.cat_H2S_list:

         for row in range(len(podp_bvo)):
             for col in range(len(podp_bvo[row])):
                 razdel_1[row+9][col] = podp_bvo[row][col]

    if CreatePZ.grpPlan == True:
        for row in range(len(podp_grp)):
            for col in range(len(podp_grp[row])):
                razdel_1[row + 12][col] = podp_grp[row][col]

    return razdel_1




