import base64
from abc import ABC, abstractmethod

import data_list
from datetime import datetime

from openpyxl.styles import Font, Alignment, Border, Side

from cdng import events_gnvp, add_itog, events_gnvp_gnkt
from main import MyMainWindow

from block_name import razdel_1, curator_sel, pop_down
from work_py.dop_plan_py import DopPlanWindow



class WorkWithPZ(ABC):
    @abstractmethod
    def open_excel_file(self, fname):
        pass


class PzInDatabase(WorkWithPZ):
    def __init__(self, parent=None):
        super(self).__init__()
        self.data_well = parent

    def open_excel_file(self):
        if 'Ойл' in data_list.contractor:
            contractor = 'ОЙЛ'
        elif 'РН' in data_list.contractor:
            contractor = 'РН'

        if self.data_well.work_plan == 'plan_change':
            DopPlanWindow.extraction_data(self, str(self.data_well.well_number.get_value) + " " +
                                          self.data_well.well_area.get_value + " " + 'krs' + " " + contractor, 1)
            self.ws.delete_rows(data_list.plan_correct_index.get_value, self.ws.max_row)
            return self.ws


class CreatePZ(MyMainWindow):
    def __init__(self, data_well, ws, parent=None):
        super(CreatePZ, self).__init__()
        self.wb = parent.wb
        self.ws = ws
        self.data_well = data_well

    def open_excel_file(self, ws, work_plan):

        if work_plan not in ['application_pvr', 'application_gis', 'gnkt_bopz', 'gnkt_opz', 'gnkt_after_grp',
                             'gnkt_frez']:
            if work_plan != 'plan_change':
                for row_ind, row in enumerate(ws.iter_rows(values_only=True, max_col=13)):
                    ws.row_dimensions[row_ind].hidden = False
                    if 'ПЛАН РАБОТ' == row[1] \
                            and work_plan == 'dop_plan':
                        ws.cell(row=row_ind + 1, column=2).value = \
                            f'ДОПОЛНИТЕЛЬНЫЙ ПЛАН РАБОТ № {self.data_well.number_dp}'

                    elif 'План-заказ' == row[1]:
                        if work_plan != 'dop_plan':
                            ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'
                        else:
                            ws.cell(row=row_ind + 1, column=2).value = \
                                f'ДОПОЛНИТЕЛЬНЫЙ ПЛАН РАБОТ № {self.data_well.number_dp}'



            if self.data_well.work_plan not in ['gnkt_frez', 'application_pvr',
                                                'application_gis', 'gnkt_after_grp', 'gnkt_opz', 'gnkt_bopz', 'plan_change']:
                # print(f'план работ {self.data_well.work_plan}')

                razdel = razdel_1(self, self.data_well.region, data_list.contractor)

                for i in range(1, len(razdel)):  # Добавлением подписантов на вверху
                    for j in range(1, 13):
                        ws.cell(row=i, column=j).value = razdel[i - 1][j - 1]
                        ws.cell(row=i, column=j).font = Font(name='Arial Cyr', size=13, bold=True)
                    ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
                    ws.merge_cells(start_row=i, start_column=8, end_row=i, end_column=12)
                    ws.row_dimensions[i].height = 20
                ws.row_dimensions[i + 1].height = 20
                ws.row_dimensions[i + 1].height = 20

                # print(f' индекс вставки ГНВП{self.data_well.insert_index}')
                dict_events_gnvp = {}
                dict_events_gnvp['krs'] = events_gnvp(self, data_list.contractor)
                dict_events_gnvp['gnkt_opz'] = events_gnvp_gnkt(self)
                dict_events_gnvp['gnkt_bopz'] = events_gnvp_gnkt(self)
                dict_events_gnvp['dop_plan'] = events_gnvp(self, data_list.contractor)
                dict_events_gnvp['prs'] = events_gnvp(self, data_list.contractor)

                # if work_plan != 'dop_plan':
                text_width_dict = {20: (0, 100), 30: (101, 200), 40: (201, 300), 60: (301, 400), 70: (401, 500),
                                   90: (501, 600), 110: (601, 700), 120: (701, 800), 130: (801, 900),
                                   150: (901, 1500), 270: (1500, 2300)}

                # Устанавливаем параметры границы
                red = 'FF0000'  # Красный цвет в формате HEX
                thin_border = Border(left=Side(style='thin', color=red),
                                     right=Side(style='thin', color=red),
                                     top=Side(style='thin', color=red),
                                     bottom=Side(style='thin', color=red))

                if work_plan != 'normir':
                    if 'Ойл' in data_list.contractor:
                        for i in range(self.data_well.insert_index,
                                       self.data_well.insert_index + len(dict_events_gnvp[work_plan])):
                            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                            data = ws.cell(row=i, column=2)
                            data.value = dict_events_gnvp[work_plan][i - self.data_well.insert_index][1]

                            if 'Мероприятия' in str(data.value) or \
                                    'Меры по предупреждению' in str(data.value) or \
                                    ' ТЕХНОЛОГИЧЕСКИЕ ПРОЦЕССЫ' in str(data.value) or \
                                    'Признаки отравления сернистым водородом' in str(data.value) or \
                                    'Контроль воздушной среды проводится:' in str(data.value) or \
                                    'Требования безопасности при выполнении работ:' in str(data.value) or \
                                    'Меры по предупреждению' in str(data.value) or \
                                    'Меры по предупреждению' in str(data.value) or \
                                    'Меры по предупреждению' in str(data.value) or \
                                    "о недопустимости нецелевого расхода" in str(data.value):
                                data.alignment = Alignment(wrap_text=True, horizontal='center',
                                                           vertical='center')
                                data.fill = data_list.yellow_fill
                                data.font = Font(name='Arial Cyr', size=13, bold=True)

                            else:
                                data.alignment = Alignment(wrap_text=True, horizontal='left',
                                                           vertical='center')

                                data.font = Font(name='Arial Cyr', size=12)
                            if not data.value is None:
                                text = data.value
                                for key, value in text_width_dict.items():
                                    if value[0] <= len(text) <= value[1]:
                                        ws.row_dimensions[i].height = int(key)

                    elif 'РН' in data_list.contractor:
                        # Устанавливаем красный цвет для текста
                        red_font = Font(name='Arial Cyr', size=13, color='FF0000', bold=True)
                        for i in range(self.data_well.insert_index,
                                       self.data_well.insert_index + len(dict_events_gnvp[work_plan])):
                            for col in range(12):
                                data = ws.cell(row=i, column=col + 1)
                                data.border = thin_border
                                data.value = dict_events_gnvp[work_plan][i - self.data_well.insert_index][col]

                                data_2 = ws.cell(row=i, column=3).value
                                data_1 = ws.cell(row=i, column=2).value
                                ws.cell(row=i, column=col + 1).font = Font(name='Arial Cyr', size=13, bold=False)

                            if 'IX.I. Мероприятия по предотвращению технологических аварий при ремонте скважин:' in \
                                    str(data_1):
                                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                               vertical='center')

                                ws.cell(row=i, column=2).font = Font(name='Arial Cyr', size=13, bold=True)
                            elif 'При работе с вертлюгами обеспечить' in str(data_2) \
                                    or 'На основании приказа' in str(data_2) \
                                    or 'Согласно мероприятий по снижению а' in str(data_2) \
                                    or 'Во время нештатных ' in str(data_2) \
                                    or 'Для предотвращения падения ' in str(data_2) \
                                    or 'После герметизации устья' in str(data_2) \
                                    or 'При свинчивании и развинчивании' in str(data_2) \
                                    or 'Сборку фрезерующего, ' in str(data_2) \
                                    or 'При нулевых и отрицательных' in str(data_2):
                                ws.merge_cells(start_row=i, start_column=3, end_row=i, end_column=11)
                                ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                               vertical='center')
                                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                               vertical='center')
                                ws.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                                vertical='center')
                                ws.cell(row=i, column=3).font = Font(name='Arial Cyr', size=13, bold=True)
                                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                               vertical='center')
                            else:
                                ws.merge_cells(start_row=i, start_column=3, end_row=i, end_column=11)
                                ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                               vertical='center')

                                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                               vertical='center')
                                ws.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                                vertical='center')
                                ws.cell(row=i, column=3).font = Font(name='Arial Cyr', size=13, bold=False)

                            if 'ВЫ ДОЛЖНЫ ОТКАЗАТЬСЯ' in str(data_2):
                                ws.cell(row=i, column=3).font = red_font

                            if not data_2 is None:
                                text = data_2
                                for key, value in text_width_dict.items():
                                    text_length = len(text)
                                    if value[0] <= text_length <= value[1]:
                                        if '\n' in text:
                                            row_dimension_value = int(len(text) / 4 + text.count('\n') * 5)
                                            ws.row_dimensions[i].height = row_dimension_value
                                        else:
                                            row_dimension_value = int(len(text) / 4)
                                            ws.row_dimensions[i].height = int(len(text) / 4)

                    self.data_well.insert_index += len(dict_events_gnvp[work_plan]) - 1

                    ws.row_dimensions[2].height = 30

                    if len(self.data_well.row_expected) != 0 and self.data_well.work_plan not in ['prs']:
                        for i in range(1, len(self.data_well.row_expected) + 1):  # Добавление показатели после ремонта
                            ws.row_dimensions[self.data_well.insert_index + i - 1].height = None
                            for j in range(1, 12):
                                if i == 1:
                                    ws.cell(row=i + self.data_well.insert_index, column=j).font = Font(
                                        name='Arial Cyr', size=13,
                                        bold=False)
                                    ws.cell(row=i + self.data_well.insert_index, column=j).alignment = Alignment(
                                        wrap_text=False,
                                        horizontal='center',
                                        vertical='center')
                                    ws.cell(row=i + self.data_well.insert_index, column=j).value = \
                                        self.data_well.row_expected[i - 1][
                                            j - 1]
                                else:
                                    ws.cell(row=i + self.data_well.insert_index, column=j).font = Font(
                                        name='Arial Cyr', size=13,
                                        bold=False)
                                    ws.cell(row=i + self.data_well.insert_index, column=j).alignment = Alignment(
                                        wrap_text=False,
                                        horizontal='left',
                                        vertical='center')
                                    ws.cell(row=i + self.data_well.insert_index, column=j).value = \
                                        self.data_well.row_expected[i - 1][
                                            j - 1]
                        ws.merge_cells(start_column=2, start_row=self.data_well.insert_index + 1, end_column=12,
                                       end_row=self.data_well.insert_index + 1)
                        self.data_well.insert_index += len(self.data_well.row_expected)
                    if work_plan not in ['application_pvr', 'gnkt_frez', 'gnkt_after_grp', 'gnkt_opz', 'gnkt_bopz',
                                         'plan_change']:
                        work_list = [
                            [None, None, 'Порядок работы', None, None, None, None, None, None, None, None, None],
                            [None, 'п/п', 'Наименование работ', None, None, None, None, None, None, None,
                             'Ответственный',
                             'Нормы времени \n мин/час.']]

                        for i in range(1, len(work_list) + 1):  # Добавление показатели после ремонта
                            for j in range(1, 13):
                                ws.cell(row=i + self.data_well.insert_index, column=j).font = Font(name='Arial Cyr',
                                                                                                   size=13,
                                                                                                   bold=True)
                                ws.cell(row=i + self.data_well.insert_index, column=j).alignment = Alignment(
                                    wrap_text=False,
                                    horizontal='center',
                                    vertical='center')
                                ws.cell(row=i + self.data_well.insert_index, column=j).value = work_list[i - 1][
                                    j - 1]
                            if i == 1:
                                ws.merge_cells(start_column=3, start_row=self.data_well.insert_index + i,
                                               end_column=12,
                                               end_row=self.data_well.insert_index + i)
                            elif i == 2:
                                ws.merge_cells(start_column=3, start_row=self.data_well.insert_index + i,
                                               end_column=10,
                                               end_row=self.data_well.insert_index + i)

                    self.insert_index_border = self.data_well.insert_index

            return ws

        elif work_plan in ['application_pvr']:
            for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
                for col_ind, col in enumerate(row):
                    if col_ind in [3, 2]:
                        if 'кровля' in str(col).lower():
                            type_pvr = ws.cell(row=row_ind, column=3).value
                            index_row_pvr_begin = row_ind + 1
                        if 'произвести контрольную' in str(col).lower():
                            index_row_pvr_cancel = row_ind
                            if index_row_pvr_begin < index_row_pvr_cancel:
                                self.data_well.index_row_pvr_list.append(
                                    (index_row_pvr_begin, index_row_pvr_cancel, type_pvr))
                                index_row_pvr_begin, index_row_pvr_cancel = 0, 0
            for pvr in self.data_well.index_row_pvr_list:
                for row in range(pvr[0], pvr[1]):
                    row_list = []
                    for col in range(2, 9):
                        row_list.append(str(ws.cell(row=row + 1, column=col + 1).value))
                    self.data_well.pvr_row_list.append(row_list)

            # print(f'Индексы ПВР {self.data_well.pvr_row_list}')

        elif work_plan in ['application_gis']:
            for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
                for col_ind, col in enumerate(row):
                    if col_ind in [3, 2]:
                        if ('задача ' in str(col).lower() or 'техкарт' in str(col).lower() or
                            'задаче №' in str(col).lower()) and \
                                'перфорация' not in str(col).lower() and 'привязка' not in str(col).lower() and \
                                'отбивка' not in str(col).lower():
                            type_pvr = ws.cell(row=row_ind + 1, column=3).value
                            self.data_well.gis_list.append(type_pvr)
        else:
            return ws

    def add_itog(self, ws, insert_index, work_plan):
        if ws.merged_cells.ranges:
            merged_cells_copy = list(ws.merged_cells.ranges)  # Создаем копию множества объединенных ячеек
            for merged_cell in merged_cells_copy:
                if merged_cell.min_row > insert_index + 5:
                    try:
                        ws.unmerge_cells(str(merged_cell))
                    except:
                        pass

        if work_plan not in ['gnkt_frez', 'application_pvr', 'gnkt_after_grp', 'gnkt_opz', 'gnkt_bopz']:
            itog_list = add_itog(self)
            for i in range(insert_index, len(itog_list) + insert_index):  # Добавлением итогов
                if i < insert_index + 6:
                    for j in range(1, 13):
                        ws.cell(row=i, column=j).value = itog_list[i - insert_index][j - 1]
                        if j != 1:
                            ws.cell(row=i, column=j).border = data_list.thin_border
                            ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)

                    ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=11)
                    ws.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                   vertical='center')
                else:
                    ws.row_dimensions[insert_index + 6].height = 50
                    ws.row_dimensions[insert_index + 8].height = 50
                    for j in range(1, 13):
                        ws.cell(row=i, column=j).value = itog_list[i - insert_index][j - 1]
                        ws.cell(row=i, column=j).border = data_list.thin_border
                        ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                        ws.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                       vertical='center')

                    ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                    ws.cell(row=i, column=j).alignment = Alignment(wrap_text=False, horizontal='left',
                                                                   vertical='center')

            insert_index += len(add_itog(self)) + 2

        curator_s = curator_sel(self.data_well.curator, self.data_well.region)
        # print(f'куратор {curator_sel, self.data_well.curator}')
        if curator_s is False:
            return

        podp_down = pop_down(self, self.data_well.region, curator_s)

        for i in range(1 + insert_index, 1 + insert_index + len(podp_down)):

            # Добавлением подписантов внизу
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = podp_down[i - 1 - insert_index][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)

            if i in range(insert_index + 7, 1 + insert_index + 15):
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=6)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=False, vertical='center', horizontal='left')
            else:
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=False, vertical='center', horizontal='left')
        ws.row_dimensions[insert_index + 7].height = 30
        ws.row_dimensions[insert_index + 9].height = 25

        insert_index += len(podp_down)
        aaa = ws.max_row

        ws.delete_rows(insert_index, aaa - insert_index)

    def is_valid_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False


def work_pz_excel_file(work_plan, parent):
    if work_plan in ['krs', 'dop_plan']:
        open_class = CreatePZ(parent)
    else:
        open_class = PzInDatabase(parent)

    return open_class

#
