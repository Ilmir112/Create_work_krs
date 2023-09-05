import datetime

import openpyxl
from copy import copy

import xlrd
from openpyxl.workbook import Workbook


def head_ind(start, finish):
    return f'A{start}:S{finish}'
def copy_row(ws, ws2, name_values, index_row, head):



    for row_number, row in enumerate(ws[head]):
        for col_number, cell in enumerate(row):
            ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1, cell.value)
            if cell.has_style:
                ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1).font = copy(cell.font)
                ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1).fill = copy(cell.fill)
                ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1).border = copy(cell.border)
                ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1).number_format = copy(
                    cell.number_format)
                ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1).protection = copy(
                    cell.protection)
                ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1).alignment = copy(
                    cell.alignment)
                ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1).quotePrefix = copy(
                    cell.quotePrefix)
                ws2.cell(row_number + 1 + len(name_values) + index_row, col_number + 1).pivotButton = copy(
                    cell.pivotButton)
    print(f'Вставлены данные по скважине')



def xls_to_xlsx(*args, **kw):
    """
    open and convert an XLS file to openpyxl.workbook.Workbook
    ----------
    @param args: args for xlrd.open_workbook
    @param kw: kwargs for xlrd.open_workbook
    @return: openpyxl.workbook.Workbook对象
    """
    book_xls = xlrd.open_workbook(*args, formatting_info=True, ragged_rows=True, **kw)
    book_xlsx = openpyxl.workbook.Workbook()

    sheet_names = book_xls.sheet_names()
    for sheet_index in range(len(sheet_names)):
        sheet_xls = book_xls.sheet_by_name(sheet_names[sheet_index])
        if sheet_index == 0:
            sheet_xlsx = book_xlsx.active
            sheet_xlsx.title = sheet_names[sheet_index]
        else:
            sheet_xlsx = book_xlsx.create_sheet(title=sheet_names[sheet_index])
        for crange in sheet_xls.merged_cells:
            rlo, rhi, clo, chi = crange
            sheet_xlsx.merge_cells(start_row=rlo + 1, end_row=rhi,
            start_column=clo + 1, end_column=chi,)

        def _get_xlrd_cell_value(cell):
            value = cell.value
            if cell.ctype == xlrd.XL_CELL_DATE:
                datetime_tup = xlrd.xldate_as_tuple(value,0)
                if datetime_tup[0:3] == (0, 0, 0):   # time format without date
                    value = datetime.time(*datetime_tup[3:])
                else:
                    value = datetime.datetime(*datetime_tup)
            return value

        for row in range(sheet_xls.nrows):
            sheet_xlsx.append((
                _get_xlrd_cell_value(cell)
                for cell in sheet_xls.row_slice(row, end_colx=sheet_xls.row_len(row))
            ))
    return book_xlsx

