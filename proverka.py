from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook
from openpyxl_image_loader import SheetImageLoader
from openpyxl.drawing.image import Image

# Load your workbook and sheet as you want, for example
wb = load_workbook('D:\python\Create_work_krs\Копия 358 ПНЛГ  (Толбазинское 358) ПНЛГ на Дпаш.xlsx')
sheet = wb.active

wb2 = Workbook()
ws2 = wb2.active

# Put your sheet in the loader
image_loader = SheetImageLoader(sheet)

image_list = []
# And get image from specified cell
for row in range(1, 166):
    for col in range(1, 10):
        try:
            image = image_loader.get(f'{get_column_letter(col)}{row}')
            image.save(f'imageFiles/image_work/image{get_column_letter(col)}{row}.png')
            logo = Image(f'imageFiles/image_work/image{get_column_letter(col)}{row}.png')
            image_list.append((f'imageFiles/image_work/image{get_column_letter(col)}{row}.png', f'{get_column_letter(col)}{row}.png', image.size))
            ws2.add_image(logo, f'{get_column_letter(col)}{row+13}')
        except:
            pass
print(image_list)



wb2.save(filename="hello_world_logo.xlsx")