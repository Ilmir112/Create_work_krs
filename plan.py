import openpyxl
from copy import copy


def copy_row(ws, ws2, name_values, index_row, head)



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

