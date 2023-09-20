import openpyxl as op
from datetime import datetime


from cdng import region_dict, region_p, events_gnvp


def region(cdng):

    region = ''.join([key for key, value in region_dict.items() if cdng in value])
    print(region)
    return region





def curator_sel(self, curator, region):
    ruk_orm = [''.join(region_p[region][2].keys()), ''.join(region_p[region][2].values())]
    ruk_pto = [''.join(region_p[region][4].keys()), ''.join(region_p[region][4].values())]
    rum_gtm = [''.join(region_p[region][3].keys()), ''.join(region_p[region][3].values())]
    ruk_usrs_krs = [''.join(region_p[region][5].keys()), ''.join(region_p[region][5].values())]
    ruk_go = [''.join(region_p[region][6].keys()), ''.join(region_p[region][6].values())]
    self.ved_gtm = [''.join(region_p[region][7].keys()), ''.join(region_p[region][7].values())]
    self.ved_orm = [''.join(region_p[region][8].keys()), ''.join(region_p[region][8].values())]

    if curator == 'ОР':
        return ruk_orm
    elif curator == 'ГТМ':
        return rum_gtm
    elif curator == 'ГО':
        return ruk_go






current_datetime = datetime.today()

def pop_down(self, region, curator_sel):
    from open_pz import CreatePZ
    nach_tkrs_list = ['А.Р.Габдулхаков ', 'З.К. Алиев', 'М.К.Алиев']
    if region == 'ЧГМ' or region == 'ТГМ':
        nach_tkrs = nach_tkrs_list[0]
    elif region == 'КГМ' or region == 'АГМ':
        nach_tkrs = nach_tkrs_list[1]
    elif region == 'ИГМ':
        nach_tkrs = nach_tkrs_list[2]


    ruk_orm = [''.join(region_p[region][2].keys()), ''.join(region_p[region][2].values())]
    ruk_pto = [''.join(region_p[region][4].keys()), ''.join(region_p[region][4].values())]
    rum_gtm = [''.join(region_p[region][3].keys()), ''.join(region_p[region][3].values())]
    ruk_usrs_krs = [''.join(region_p[region][5].keys()), ''.join(region_p[region][5].values())]
    ruk_go = [''.join(region_p[region][6].keys()), ''.join(region_p[region][6].values())]
    ved_gtm = [''.join(region_p[region][7].keys()), ''.join(region_p[region][7].values())]
    ved_orm = [''.join(region_p[region][8].keys()), ''.join(region_p[region][8].values())]


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
        [None, ruk_pto[0], None, None, None, None, None, None, None,
         ruk_pto[1], None, ' '],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, ruk_usrs_krs[0], None, None, None, None,
         None, None, None, ruk_usrs_krs[1], None, None],
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

    ved_gtm_list = [None, ved_gtm[0], None, None, None, None,  '"___"___________' , None, None, ved_gtm[1], None, None]

    ved_orm_list = [None, ved_orm[0], None, None, None, None, '"___"___________', None, None, ved_orm[1], None, None]
    if (region == 'ЧГМ' or region == 'КГМ') and CreatePZ.curator == 'ОР':
        print(pop_down)
        podp_down.insert(13, ved_orm_list)
    elif region == 'КГМ' or region == 'ЧГМ' and CreatePZ.curator == 'ГТМ':
        podp_down.insert(13, ved_gtm_list)


    return podp_down


def razdel_1(self, region):
    from open_pz import CreatePZ

    gi_region = [''.join(region_p[region][0].keys()), ''.join(region_p[region][0].values())]
    gg_region = [''.join(region_p[region][1].keys()), ''.join(region_p[region][1].values())]
    razdel_1 = [[None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
                [None, gi_region[0], None, None, None, None, None,
                  'Главный Инженер ООО "Ойл-Сервис"', None, None, None, None],
                [None, f'____________{gi_region[1]}', None, None, None, None, None,
                 '_____________А.Р. Хасаншин', None, None, None, None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None,
                 f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, gg_region[0], None, None, None,
                 None,
                 None, 'Главный геолог ООО "Ойл-Сервис"', None, None, None, None],
                [None, f'_____________{gg_region[1]}', None, None, None, None,  None,
                 '_____________Д.Д. Шамигулов', None, None,'',
                 None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, '', None, None,
                 f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
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
        razdel_1.append(podp_bvo)
    return razdel_1




