from datetime import datetime

import data_list
from cdng import REGION_BASHNEFT_DICT
import json


def region_select(cdng):
    region_work = ''.join([key for key, value in REGION_BASHNEFT_DICT.items() if cdng in value])
    return region_work


# выбор подписантов в зависимости от вида ГТМ
def curator_sel(curator, region):

    with open(f'{data_list.path_image}podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)
    if curator == 'ОР':
        return (podpis_dict[data_list.costumer][region]['ruk_orm']['post'], podpis_dict[data_list.costumer][region]["ruk_orm"]['surname'])
    elif curator == 'ГТМ':
        return (podpis_dict[data_list.costumer][region]["ruk_gtm"]['post'], podpis_dict[data_list.costumer][region]["ruk_gtm"]['surname'])
    elif curator == 'ГО':
        return (podpis_dict[data_list.costumer][region]['go']['post'], podpis_dict[data_list.costumer][region]["go"]['surname'])
    elif curator == 'ВНС':
        return (podpis_dict[data_list.costumer][region]['go']['post'], podpis_dict[data_list.costumer][region]["go"]['surname'])
    elif curator == 'ГРР':
        return (podpis_dict[data_list.costumer][region]['grr']['post'], podpis_dict[data_list.costumer][region]["grr"]['surname'])
    return False


current_datetime = datetime.today()


# Выбор подписантов в зависимости от региона
def pop_down(self, region, curator_sel):

    with open(f'{data_list.path_image}podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)
    nach_list = ''
    if 'Ойл' in data_list.contractor:
        nach_tkrs = ''
        nach_tkrs_post = ''
        if region == 'ЧГМ' or region == 'ТГМ' or 'gnkt' in self.data_well.work_plan:
            nach_tkrs = podpis_dict[data_list.contractor]['Экспедиция']["ЦТКРС №1"]["сhief_engineer"]["surname"]
            nach_tkrs_post = podpis_dict[data_list.contractor]['Экспедиция']["ЦТКРС №1"]["сhief_engineer"]["post"]
        elif region == 'КГМ' or region == 'АГМ':
            nach_tkrs = podpis_dict[data_list.contractor]['Экспедиция']["ЦТКРС №2"]["сhief_engineer"]["surname"]
            nach_tkrs_post = podpis_dict[data_list.contractor]['Экспедиция']["ЦТКРС №2"]["сhief_engineer"]["post"]
        elif region == 'ИГМ':
            nach_tkrs = podpis_dict[data_list.contractor]['Экспедиция']["ЦТКРС №4"]["сhief_engineer"]["surname"]
            nach_tkrs_post = podpis_dict[data_list.contractor]['Экспедиция']["ЦТКРС №4"]["сhief_engineer"]["post"]

        nach_list = [
            [None, f'План работ составил {data_list.user[0]}', None, None, None, None, '___________________', None,
             None,
             f'{data_list.user[1]}', None, None],
            [None, None, None, None, None, None, None, None, 'дата составления', None,
             datetime.now().strftime('%d.%m.%Y'),
             None],
            [None, None, f'{nach_tkrs_post}', None, None, None, None, None, None,
             nach_tkrs, None, None],
            [None, None, None, None, None, None, None, None, None, '     дата подписания', None, None]]
    elif "РН" in data_list.contractor:
        nach_list = [
            [None, f'План работ составил {data_list.user[0]}', None, None, None, None, '___________________', None,
             None,
             f'{data_list.user[1]}', None, None],
            [None, None, None, None, None, None, None, None, 'дата составления', None,
             datetime.now().strftime('%d.%m.%Y'),
             None]]

    with open(f'{data_list.path_image}podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)

    podp_down = [
        [None, ' ', 'Согласовано:', None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, '', None, None, '', None, None],
        [None, curator_sel[0], None, None, None, None, '___________________', None, None,
         curator_sel[1], None, None],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, podpis_dict[data_list.costumer][region]['ruk_pto']['post'], None, None, None, None, '___________________', None,
         None,
         podpis_dict[data_list.costumer][region]["ruk_pto"]['surname'], None, ' '],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, podpis_dict[data_list.costumer][region]['usrs']['post'], None, None, None, None,
         '___________________', None, None, podpis_dict[data_list.costumer][region]['usrs']['surname'], None, None],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, None, None, None, None, None, None, None, None, None, None, None],

        [None, 'Замечания:', None, None, None, None, None, None, None, None, None, None],
        [None, '1.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '2.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '3.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '4.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '5.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, None, None, 'Проинструктированы, с планом работ ознакомлены:                         ', None,
         None, None, None, None, None, None, None],
        [None, None, 'Мастер бригады', None, None, None, f'Инструктаж провел мастер бригады {data_list.contractor}',
         None, None, None, None, None],
        [None, None, 'Мастер бригады', None, None, None, None, None, None, None, 'подпись', None],
        [None, f'Бурильщик {data_list.contractor}', None, None,
         f'_____________________Бурильщик {data_list.contractor}________________________', None, None, None, None,
         None, None, None],
        [None, f'Пом.бур-ка {data_list.contractor}', None, None,
         f'_____________________Пом.бур-ка {data_list.contractor}_______________________', None, None, None, None,
         None, None, None],
        [None, f'Пом.бур-ка {data_list.contractor}', None, None,
         f'_____________________Пом.бур-ка {data_list.contractor}_______________________', None, None, None, None,
         None, None, None],
        [None, None, 'Машинист', None,
         '_____________________ Машинист ________________________', None, None, None,
         None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None]]

    for row in nach_list[::-1]:
        podp_down.insert(0, row)

    ved_gtm_list = [None, podpis_dict[data_list.costumer][region]['ved_gtm']['post'], None, None, None, None, '_______________',
                    None, None,
                    podpis_dict[data_list.costumer][region]['ved_gtm']['surname'], None, None]

    ved_orm_list = [None, podpis_dict[data_list.costumer][region]['ved_orm']['post'], None, None, None, None, '_______________',
                    None, None,
                    podpis_dict[data_list.costumer][region]['ved_orm']['surname'], None, None]
    if (region == 'ЧГМ') and self.data_well.curator == 'ОР':
        podp_down.insert(13, ved_orm_list)
        podp_down.insert(14,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    elif (region == 'КГМ') and self.data_well.curator == 'ОР' and self.data_well.work_plan == 'gnkt_opz':

        podp_down.insert(12, ved_orm_list)
        podp_down.insert(13,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    elif (region == 'КГМ') and self.data_well.curator == 'ОР':

        podp_down.insert(12, ved_gtm_list)
        podp_down.insert(13,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    elif region == 'КГМ' or region == 'ЧГМ' and self.data_well.curator == 'ГТМ':
        podp_down.insert(12, ved_gtm_list)
        podp_down.insert(13,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    elif region == 'КГМ' or region == 'ЧГМ' and self.data_well.curator == 'ГТМ':
        podp_down.insert(12, ved_gtm_list)
        podp_down.insert(13,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    if self.data_well.curator == "ВНС":
        podp_down.insert(6, [None, 'Менеджер ТКРС БНД', None, None, None, None, '___________________', None, None,
                             'А.М. Кузьмин', None, ' '])
        podp_down.insert(7,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])

    return podp_down


