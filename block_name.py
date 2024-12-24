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
            nach_tkrs = podpis_dict[data_list.contractor]["ЦТКРС №1"]["начальник"]["surname"]
            nach_tkrs_post = podpis_dict[data_list.contractor]["ЦТКРС №1"]["начальник"]["post"]
        elif region == 'КГМ' or region == 'АГМ':
            nach_tkrs = podpis_dict[data_list.contractor]["ЦТКРС №2"]["начальник"]["surname"]
            nach_tkrs_post = podpis_dict[data_list.contractor]["ЦТКРС №2"]["начальник"]["post"]
        elif region == 'ИГМ':
            nach_tkrs = podpis_dict[data_list.contractor]["ЦТКРС №4"]["начальник"]["surname"]
            nach_tkrs_post = podpis_dict[data_list.contractor]["ЦТКРС №4"]["начальник"]["post"]

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


def razdel_1(self, region, contractor):
    with open(f'{data_list.path_image}podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)
    razdel_1 = ''
    if 'prs' in self.data_well.work_plan:
        if 'Ойл' in contractor:
            if region == 'ЧГМ' or region == 'ТГМ' or 'gnkt' in self.data_well.work_plan:
                data_list.ctkrs = "ЦТКРС №1"
            elif region == 'КГМ' or region == 'АГМ':
                data_list.ctkrs = "ЦТКРС №2"
            elif region == 'ИГМ':
                data_list.ctkrs = 'ЦТКРС №4'

        nach_cdng_post = podpis_dict[data_list.costumer][self.data_well.region]["ЦДНГ"][self.data_well.cdng.get_value]['Начальник']['post'] + ' ' + self.data_well.cdng.get_value
        nach_cdng_name = podpis_dict[data_list.costumer][self.data_well.region]["ЦДНГ"][self.data_well.cdng.get_value]['Начальник']["surname"]
        nach_cdng_name = nach_cdng_name.split(' ')
        nach_cdng_name = f'{nach_cdng_name[0]} {nach_cdng_name[1][0]}.{nach_cdng_name[1][0]}.'
        technol_cdng_post = podpis_dict[data_list.costumer][self.data_well.region]["ЦДНГ"][self.data_well.cdng.get_value]['Ведущий инженер-технолог']['post'] + ' ' + self.data_well.cdng.get_value
        technol_cdng_name = podpis_dict[data_list.costumer][self.data_well.region]["ЦДНГ"][self.data_well.cdng.get_value]['Ведущий инженер-технолог']["surname"]
        technol_cdng_name = technol_cdng_name.split(' ')
        technol_cdng_name = f'{technol_cdng_name[0]} {technol_cdng_name[1][0]}.{technol_cdng_name[1][0]}.'
        geolog_cdng_post = podpis_dict[data_list.costumer][self.data_well.region]["ЦДНГ"][self.data_well.cdng.get_value]['Ведущий геолог']['post'] + ' ' + self.data_well.cdng.get_value
        geolog_cdng_name = podpis_dict[data_list.costumer][self.data_well.region]["ЦДНГ"][self.data_well.cdng.get_value]['Ведущий геолог']["surname"]
        geolog_cdng_name = geolog_cdng_name.split(' ')
        geolog_cdng_name = f'{geolog_cdng_name[0]} {geolog_cdng_name[1][0]}.{geolog_cdng_name[1][0]}.'
        nach_ctkrs_post = podpis_dict[data_list.contractor][data_list.ctkrs]['начальник']['post']
        nach_ctkrs_name = podpis_dict[data_list.contractor][data_list.ctkrs]['начальник']["surname"]


        razdel_1 = [
            [None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
            [None, nach_cdng_post, None, None, None, None, None, nach_ctkrs_post, None, None, None, None],
            [None, f'____________{nach_cdng_name}',
             None, None, None, None, None,
             f'_____________{nach_ctkrs_name}', None, None, None, None],
            [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None,
             f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None,
             technol_cdng_post,
             None, None, None, None, None, None, None, None, None, None],
            [None,
             f'____________{technol_cdng_name}',
             None, None, None, None, None, None, None, None, None, None],
            [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None,
             None, None, None, None, None],
            [None,
             geolog_cdng_post,
             None, None, None, None, None, None, None, None, None, None],
            [None,
             f'____________{geolog_cdng_name}',
             None, None, None, None, None, None, None, None, None, None],
            [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None]]

    elif 'Ойл' in contractor:

        razdel_1 = [
            [None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
            [None, podpis_dict[data_list.costumer][region]['gi']['post'], None, None, None, None, None,
             f'{podpis_dict[data_list.contractor]["сhief_engineer"]["post"]}', None, None, None, None],
            [None, f'____________{podpis_dict[data_list.costumer][region]["gi"]["surname"]}', None, None, None, None, None,
             f'_____________{podpis_dict[data_list.contractor]["сhief_engineer"]["surname"]}', None, None, None, None],
            [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None,
             f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, podpis_dict[data_list.costumer][region]['gg']['post'], None, None, None,
             None,
             None, f'{podpis_dict[data_list.contractor]["chief_geologist"]["post"]}', None, None, None, None],
            [None, f'_____________{podpis_dict[data_list.costumer][region]["gg"]["surname"]}', None, None, None, None, None,
             f'_____________{podpis_dict[data_list.contractor]["chief_geologist"]["surname"]}', None, None, '',
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
    elif 'РН' in contractor:
        razdel_1 = [
            [None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
            [None, podpis_dict[data_list.costumer][region]['gi']['post'], None, None, None, None, None,
             f'Главный Инженер Экспедиции № 5 {data_list.contractor} филиал г. Уфа ', None, None, None, None],
            [None, f'____________{podpis_dict[data_list.costumer][region]["gi"]["surname"]}', None, None, None, None, None,
             '_____________А.А. Фаррахов ', None, None, None, None],
            [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None,
             f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
            [None, None, None, None, None, None,
             None, None, None,
             None, None, None],
            [None, podpis_dict[data_list.costumer][region]['gg']['post'], None, None, None,
             None,
             None, f'Главный геолог Экспедиции № 5 {data_list.contractor} филиал г.Уфа', None, None, None, None],

            [None, f'_____________{podpis_dict[data_list.costumer][region]["gg"]["surname"]}', None, None, None, None, None,
             f'_____________Е.А. Самойлова', None, None, '',
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
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None]]

    podp_grp = [[None, 'Представитель подрядчика по ГРП', None, None, None, None, None, None, None, None, None,
                 None],
                [None, '_____________', None, None, None, None, None, None, None, None, None, None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
                 None, None, None,
                 None]]
    podp_bvo = [
        [None, 'Районный инженер Башкирского ', None, None, None, None, None, None, None, None, None, None],
        [None, 'военизированного отряда ', None, None, None, None, None, None, None, None, None, None],
        [None, '_____________', None, None, None, None, None, None, None, None, None, None],
        [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
         None, None, None,
         None]]
    if data_list.data_in_base is False:

        if len(self.data_well.plast_work) != 0:
            # print(self.data_well.plast_work, self.data_well.dict_category)
            try:
                cat_P_1 = self.data_well.dict_category[self.data_well.plast_work[0]]['по давлению'].category
                category_h2s_list = self.data_well.dict_category[self.data_well.plast_work[0]]['по сероводороду'].category
                cat_gaz = self.data_well.dict_category[self.data_well.plast_work[0]]['по газовому фактору'].category
            except:
                cat_P_1 = self.data_well.category_pressure_well[0]
                category_h2s_list = self.data_well.category_h2s_list[0]
                cat_gaz = self.data_well.category_gaz_factor_percent[0]
        else:

            cat_P_1 = self.data_well.category_pressure_well[0]
            category_h2s_list = self.data_well.category_h2s_list[0]
            cat_gaz = self.data_well.category_gaz_factor_percent[0]
        try:
            cat_P_1_plan = self.data_well.dict_category[self.data_well.plast_project[0]]['по давлению'].category
            category_h2s_list_plan = self.data_well.dict_category[self.data_well.plast_project[0]]['по сероводороду'].category
            cat_gaz_plan = self.data_well.dict_category[self.data_well.plast_project[0]]['по газовому фактору'].category
        except:
            cat_P_1_plan = 3
            category_h2s_list_plan = 3
            cat_gaz_plan = 3

        if 1 in [cat_P_1, cat_P_1_plan, category_h2s_list, cat_gaz, category_h2s_list_plan, cat_gaz_plan,
                 self.data_well.category_pressure] or '1' in [cat_P_1, cat_P_1_plan, category_h2s_list, cat_gaz,
                                                         category_h2s_list_plan, cat_gaz_plan,
                                                         self.data_well.category_pressure] or \
                self.data_well.curator == 'ВНС':
            for row in range(len(podp_bvo)):
                for col in range(len(podp_bvo[row])):
                    razdel_1[row + 9][col] = podp_bvo[row][col]


        if self.data_well.grp_plan is True:
            for row in range(len(podp_grp)):
                for col in range(len(podp_grp[row])):
                    razdel_1[row + 13][col] = podp_grp[row][col]

    return razdel_1