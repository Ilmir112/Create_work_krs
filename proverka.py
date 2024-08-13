
from openpyxl.reader.excel import load_workbook

fname = 'property_excel/template_normir_new.xlsm'

if fname:
    wb_summary = load_workbook(fname)
    ws_summary = wb_summary.active
    print(ws_summary)

    normir_list = []
    for row_ind, row in enumerate(ws_summary.iter_rows(max_col=32)):
        list = []
        if row_ind < 46:
            for col, value in enumerate(row):
                list.append(value.value)
            normir_list.append(list)

for row in normir_list:
    print(row, sep='/n,')

