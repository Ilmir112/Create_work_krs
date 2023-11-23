from openpyxl import Workbook
from openpyxl.drawing.image import Image
from PIL import Image as PILImage

# Создаем новую книгу
workbook = Workbook()
sheet = workbook.active

# Загружаем изображение с помощью библиотеки Pillow
img = PILImage.open('example.png')

# Сохраняем изображение во временном файле
img_path = 'temp.png'
img.save(img_path)

# Вставляем изображение в Excel-документ
img = Image(img_path)
sheet.add_image(img, 'A1')

# Сохраняем книгу в файл
workbook.save('example.xlsx')
filename = 'imageFiles/Зуфаров.png'
insert_image(filename, cell_coordinates='B3')

wb.save('example.xlsx') # сохраняем файл