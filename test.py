import re

# Путь к вашему файлу с кодом
input_file_path = 'data_correct.py'  # замените на путь к вашему файлу
output_file_path = 'data_correct2.py'  # результат сохраните сюда

# Смещение номера строки (например, +1)
line_offset = 2

# Регулярное выражение для поиска вызовов addWidget
# Оно ищет строки вида: self.grid.addWidget(..., ..., ...)
pattern = re.compile(
    r'(self\.grid\.addWidget$)\s*'          # начало вызова
    r'([^)]+?)\s*,'                         # аргументы до номера строки
    r'\s*(\d+)\s*,'                         # номер строки
    r'\s*([^)]+?)$'                        # оставшиеся аргументы
)


with open(input_file_path, 'r', encoding='utf-8') as file:
    code = file.read()

def replace_line_number(match):
    prefix = match.group(1)  # 'self.grid.addWidget('
    args_before_line = match.group(2)  # аргументы перед номером строки
    line_number_str = match.group(3)   # номер строки как строка
    args_after_line = match.group(4)   # остальные аргументы

    line_number = int(line_number_str)
    new_line_number = line_number + line_offset

    return f"{prefix}{args_before_line}, {new_line_number}, {args_after_line})"

# Заменяем все совпадения
new_code = pattern.sub(replace_line_number, code)

# Сохраняем результат
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(new_code)

print(f"Обработка завершена. Результат сохранен в {output_file_path}")