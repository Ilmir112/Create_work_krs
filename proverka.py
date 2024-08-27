
# from openpyxl.reader.excel import load_workbook
#
from work_py.alone_oreration import volume_jamming_well, volume_nkt_metal
import well_data
#
# fname = 'property_excel/template_normir_new.xlsm'
#
# if fname:
#     wb_summary = load_workbook(fname)
#     ws_summary = wb_summary.active
#     print(ws_summary)
#
#     normir_list = []
#     for row_ind, row in enumerate(ws_summary.iter_rows(min_col=58, max_col=66)):
#         list = []
#         if row_ind < 46:
#             for col, value in enumerate(row):
#                 list.append(value.value)
#             normir_list.append(list)
#
# for row in normir_list:
#     print(row, sep='/n,')
well_data.column_diametr._value,  well_data.column_wall_thickness._value = 146, 8
volume_well_30 = volume_jamming_well(None, 30) / 1.1
nkt_edit = '73'
if '73' in str(nkt_edit):
    volume_nkt_metal = 1.17 * 1.0 / 1000
elif '60' in str(nkt_edit):
    volume_nkt_metal = 0.87 * 1.0 / 1000
elif '89' in str(nkt_edit):
    volume_nkt_metal = 1.7 * 1.0 / 1000
elif '48' in str(nkt_edit):
    volume_nkt_metal = 0.55 * 1.0 / 1000
lenght_nkt = volume_well_30 / volume_nkt_metal

print(lenght_nkt)
