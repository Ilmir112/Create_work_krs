import json
from data_list import current_date, path_image, user, path_image,costumer, data_in_base, contractor

def check_if_none(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, float):
        return value

    elif str(value).replace(".", "").replace(",", "").isdigit():
        if str(round(float(str(value).replace(",", ".")), 1))[-1] == "0":
            return int(float(str(value).replace(",", ".")))
        else:
            return float(str(value).replace(",", "."))
    else:
        return 0

def work_podpisant_list(data_well):
    with open(
            f"{path_image}podpisant.json", "r", encoding="utf-8"
    ) as file:
        podpis_dict = json.load(file)

    power_of_attorney = None
    expedition = ""
    if "Ойл" in contractor:
        chief_engineer_post = podpis_dict[contractor]["Руководство"][
            "chief_engineer"
        ]["post"]
        chief_engineer_surname = podpis_dict[contractor]["Руководство"][
            "chief_engineer"
        ]["surname"]
        chief_geologist_post = podpis_dict[contractor]["Руководство"][
            "chief_geologist"
        ]["post"]
        chief_geologist_surname = podpis_dict[contractor]["Руководство"][
            "chief_geologist"
        ]["surname"]
    elif "РН" in contractor:
        number_expedition = [
            number for number in user[0] if number.isdigit()
        ][0]
        if data_well.region == "ТГМ":
            expedition = f"Экспедиция № 3"
        elif data_well.region == "ЧГМ":
            expedition = f"Экспедиция № 2"
        elif data_well.region == "АГМ":
            expedition = f"Экспедиция № 5"
        elif data_well.region == "ИГМ":
            expedition = f"Экспедиция № 1"
        elif data_well.region == "КГМ":
            expedition = f"Экспедиция № 4"

        chief_engineer_post = podpis_dict[contractor]["Экспедиция"][
            expedition
        ]["chief_engineer"]["post"]
        chief_engineer_surname = podpis_dict[contractor]["Экспедиция"][
            expedition
        ]["chief_engineer"]["surname"]
        power_of_attorney = podpis_dict[contractor]["Экспедиция"][
            expedition
        ]["chief_engineer"]["power_of_attorney"]
        chief_geologist_post = podpis_dict[contractor]["Экспедиция"][
            expedition
        ]["chief_geologist"]["post"]
        chief_geologist_surname = podpis_dict[contractor]["Экспедиция"][
            expedition
        ]["chief_geologist"]["surname"]

        work_podpisant_list = [
            [
                None, "СОГЛАСОВАНО:",
                None, None, None, None, None,
                "УТВЕРЖДАЕМ:", None, None, None, None,
            ],
            [
                None,
                podpis_dict[costumer][data_well.region]["gi"]["post"], None, None, None, None, None,
                chief_engineer_post, None, None, None, None,
            ],
            [
                None,
                f'____________{podpis_dict[costumer][data_well.region]["gi"]["surname"]}', None, None, None, None,
                None,
                f"_____________{chief_engineer_surname}", None, None, None, None,
            ],
            [
                None,
                f'"____"_____________________{current_date.year}г.', None, None, None, None, None,
                f'"____"_____________________{current_date.year}г.', None, None, None, None,
            ],
            [None, None, None, None, None, None, None,
             power_of_attorney, None, None, None, None,
             ],
            [
                None,
                podpis_dict[costumer][data_well.region]["gg"]["post"], None, None, None, None, None, None, None,
                None, None, None,
            ],
            [
                None,
                f'_____________{podpis_dict[costumer][data_well.region]["gg"]["surname"]}', None, None, None, None,
                None, None, None, None,
                "", None,
            ],
            [
                None,
                f'"____"_____________________{current_date.year}г.', None, None,
                "", None, None, None, None, None, None, None,
            ],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             ],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             ],
            [
                None, None, None, None, None, None,
                None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None,
             ],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             ],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             ],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             ],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             ],
        ]

        if "3" in expedition or "2" in expedition:
            work_podpisant_list[5] = [
                None,
                podpis_dict[costumer][data_well.region]["gg"]["post"],
                None, None, None, None, None, None, None, None, None, None,
            ]
            work_podpisant_list[6] = [
                None,
                f'_____________{podpis_dict[costumer][data_well.region]["gg"]["surname"]}',
                None, None, None, None, None, None, None, None,
                "", None,
            ]
            work_podpisant_list[7] = [
                None,
                f'"____"_____________________{current_date.year}г.', None, None,
                "", None, None, None, None, None, None, None,
            ]

    if "prs" in data_well.work_plan:
        if "Ойл" in contractor:
            if (
                    data_well.region == "ЧГМ"
                    or data_well.region == "ТГМ"
                    or "gnkt" in data_well.work_plan
            ):
                ctkrs = "ЦТКРС №1"
            elif data_well.region == "КГМ" or data_well.region == "АГМ":
                ctkrs = "ЦТКРС №2"
            elif data_well.region == "ИГМ":
                ctkrs = "ЦТКРС №4"

        nach_cdng_post = (
                podpis_dict[costumer][data_well.region]["ЦДНГ"][
                    data_well.cdng.get_value
                ]["Начальник"]["post"]
                + " "
                + data_well.cdng.get_value
        )
        nach_cdng_name = podpis_dict[costumer][data_well.region][
            "ЦДНГ"
        ][data_well.cdng.get_value]["Начальник"]["surname"]
        nach_cdng_name = nach_cdng_name.split(" ")
        nach_cdng_name = (
            f"{nach_cdng_name[0]} {nach_cdng_name[1][0]}.{nach_cdng_name[1][0]}."
        )
        technol_cdng_post = (
                podpis_dict[costumer][data_well.region]["ЦДНГ"][
                    data_well.cdng.get_value
                ]["Ведущий инженер-технолог"]["post"]
                + " "
                + data_well.cdng.get_value
        )
        technol_cdng_name = podpis_dict[costumer][data_well.region][
            "ЦДНГ"
        ][data_well.cdng.get_value]["Ведущий инженер-технолог"]["surname"]
        technol_cdng_name = technol_cdng_name.split(" ")
        technol_cdng_name = f"{technol_cdng_name[0]} {technol_cdng_name[1][0]}.{technol_cdng_name[1][0]}."
        geolog_cdng_post = (
                podpis_dict[costumer][data_well.region]["ЦДНГ"][
                    data_well.cdng.get_value
                ]["Ведущий геолог"]["post"]
                + " "
                + data_well.cdng.get_value
        )
        geolog_cdng_name = podpis_dict[costumer][data_well.region][
            "ЦДНГ"
        ][data_well.cdng.get_value]["Ведущий геолог"]["surname"]
        geolog_cdng_name = geolog_cdng_name.split(" ")
        geolog_cdng_name = f"{geolog_cdng_name[0]} {geolog_cdng_name[1][0]}.{geolog_cdng_name[1][0]}."
        nach_ctkrs_post = podpis_dict[contractor]["Экспедиция"][ctkrs]["chief_engineer"]["post"]
        nach_ctkrs_name = podpis_dict[contractor]["Экспедиция"][ctkrs]["chief_engineer"]["surname"]

        work_podpisant_list = [
            [None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
            [None, nach_cdng_post, None, None, None, None, None, nach_ctkrs_post, None, None, None, None],
            [None, f'____________{nach_cdng_name}',
             None, None, None, None, None,
             f'_____________{nach_ctkrs_name}', None, None, None, None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, None, None, None,
             f'"____"_____________________{current_date.year}г.', None, None, None, None],
            [None, None, None, None, " ", None, None, None, None, None, None, None],
            [None,
             technol_cdng_post,
             None, None, None, None, None, None, None, None, None, None],
            [None,
             f'____________{technol_cdng_name}',
             None, None, None, None, None, None, None, None, None, None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, None, None, None,
             None, None, None, None, None],
            [None,
             geolog_cdng_post,
             None, None, None, None, None, None, None, None, None, None],
            [None,
             f'____________{geolog_cdng_name}',
             None, None, None, None, None, None, None, None, None, None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, None, None, None,
             None, None, None, None, None]]

    elif "krs" in data_well.work_plan and data_well.curator == "ВНС":
        work_podpisant_list = [
            [None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
            [None, "Первый заместитель генерального директора -\n главный инженер ООО 'Башнефть-Добыча'  ",
             None, None, None, None, None,
             chief_engineer_post, None, None, None, None],
            [None, f'_________________________Д.А.Чувакин', None, None, None,
             None, None,
             f'_____________{chief_engineer_surname}', None, None, None,
             None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, None, None, None,
             f'"____"_____________________{current_date.year}г.', None, None, None, None],
            [None, None, None, None, " ", None, None, None, None, None, None, None],
            [None, 'Заместитель генерального директора - \nглавный геолог  ООО "Башнефть-Добыча"  ', None, None,
             None,
             None, None, f'{chief_geologist_post}', None, None, None, None],
            [None, f'__________________________И.Р. Баширов ', None, None, None, None, None,
             f'_____________{chief_geologist_surname}', None, None, '',
             None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, '', None, None,
             f'"____"_____________________{current_date.year}г.', None, None, None, None],
            [None, None, None, None, " ", None, None, None, None, None, None, None],
            [None, 'Начальник управления добычи нефти и газа ООО "Башнефть-Добыча" ', None, None, None,
             None, None, None, None,
             None, None, None],
            [None, f'__________________________М.А.Тенюнин', None, None, None,
             None, None, None, None, None, None, None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, '', None, None,
             None, None, None, None, None],
            [None, None, None, None, " ", None, None, None, None, None, None, None],
            [None, 'Начальник отдела-заместитель начальника Управления супервайзинга \nремонта скважин и '
                   'скважинных технологий ООО "Башнефть-Добыча"', None, None, None, None, None, None, None,
             None, None, None],
            [None, f'__________________________А.Ю.Пензин', None, None, None,
             None, None, None, None, None, None, None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, '', None, None,
             None, None, None, None, None],
            [None, None, None, None, " ", None, None, None, None, None, None, None],
            [None, podpis_dict[costumer][data_well.region]['gi']['post'], None, None, None, None, None,
             None, None, None, None, None],
            [None, f'____________{podpis_dict[costumer][data_well.region]["gi"]["surname"]}', None, None, None,
             None, None, None, None, None, None, None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, None, None, None,
             None, None, None, None, None],
            [None, None, None, None, None, None, None, power_of_attorney, None, None, None, None],
            [None, podpis_dict[costumer][data_well.region]['gg']['post'], None, None, None,
             None, None, None, None, None, None, None],
            [None, f'_____________{podpis_dict[costumer][data_well.region]["gg"]["surname"]}', None, None, None,
             None, None, None, None, None, None, None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, '', None, None,
             None, None, None, None, None],
        ]

    else:
        work_podpisant_list = [
            [None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
            [None, podpis_dict[costumer][data_well.region]['gi']['post'], None, None, None, None, None,
             chief_engineer_post, None, None, None, None],
            [None, f'____________{podpis_dict[costumer][data_well.region]["gi"]["surname"]}', None, None, None,
             None, None,
             f'__________________________{chief_engineer_surname}', None, None, None,
             None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, None, None, None,
             f'"____"_____________________{current_date.year}г.', None, None, None, None],
            [None, None, None, None, None, None, None, power_of_attorney, None, None, None, None],
            [None, podpis_dict[costumer][data_well.region]['gg']['post'], None, None, None,
             None, None, f'{chief_geologist_post}', None, None, None, None],
            [None, f'_____________{podpis_dict[costumer][data_well.region]["gg"]["surname"]}', None, None, None,
             None,
             None,
             f'__________________________{chief_geologist_surname}', None, None, '',
             None],
            [None, f'"____"_____________________{current_date.year}г.', None, None, '', None, None,
             f'"____"_____________________{current_date.year}г.', None, None, None, None],
        ]

    podp_bvo = [
        [None, None, None, None, " ", None, None, None, None, None, None, None],
        [None, 'Районный инженер Башкирского ', None, None, None, None, None, None, None, None, None, None],
        [None, 'военизированного отряда ', None, None, None, None, None, None, None, None, None, None],
        [None, '__________________________', None, None, None, None, None, None, None, None, None, None],
        [None, f'"____"_____________________{current_date.year}г.', None, None, None, None, None, None,
         None, None, None,
         None],
        [None, None, None, None, " ", None, None, None, None, None, None, None]]

    if data_in_base is False:
        if len(data_well.plast_work) != 0:

            try:
                cat_P_1 = data_well.dict_category[
                    data_well.plast_work[0]
                ]["по давлению"].category
                category_h2s_list = data_well.dict_category[
                    data_well.plast_work[0]
                ]["по сероводороду"].category
                cat_gaz = data_well.dict_category[
                    data_well.plast_work[0]
                ]["по газовому фактору"].category
            except:
                cat_P_1 = data_well.category_pressure_well[0]
                category_h2s_list = data_well.category_h2s_list[0]
                cat_gaz = data_well.category_gaz_factor_percent[0]
        else:
            cat_P_1 = data_well.category_pressure_well[0]
            category_h2s_list = data_well.category_h2s_list[0]
            cat_gaz = data_well.category_gaz_factor_percent[0]
        try:
            cat_P_1_plan = data_well.dict_category[
                data_well.plast_project[0]
            ]["по давлению"].category
            category_h2s_list_plan = data_well.dict_category[
                data_well.plast_project[0]
            ]["по сероводороду"].category
            cat_gaz_plan = data_well.dict_category[
                data_well.plast_project[0]
            ]["по газовому фактору"].category
        except:
            cat_P_1_plan = 3
            category_h2s_list_plan = 3
            cat_gaz_plan = 3

        if (
                1
                in [
            cat_P_1,
            cat_P_1_plan,
            category_h2s_list,
            cat_gaz,
            category_h2s_list_plan,
            cat_gaz_plan,
            data_well.category_pressure,
        ]
                or "1"
                in [
            cat_P_1,
            cat_P_1_plan,
            category_h2s_list,
            cat_gaz,
            category_h2s_list_plan,
            cat_gaz_plan,
            data_well.category_pressure,
        ]
                or data_well.curator == "ВНС"
        ):
            work_podpisant_list.extend(podp_bvo)

    work_podpisant_list.extend([
        [None, None, None, None, " ", None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None]])

    return work_podpisant_list
