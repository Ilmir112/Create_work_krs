# -*- coding: utf-8 -*-
"""Перед сохранением Excel: ISO-строка даты -> значение date + формат ячейки."""
import re
from datetime import date

_ISO_DATE_ONLY = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})\s*$")
# Отображение как 05.12.2025 (свойство ячейки в Excel)
DATE_DISPLAY_FORMAT = "dd.mm.yyyy"


def normalize_workbook_iso_date_strings(workbook):
    """
    Если значение ячейки — строка вида YYYY-MM-DD: записать date и number_format.
    Не трогает неполные совпадения в длинных строках и невалидные даты.
    """
    for ws in workbook.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                val = cell.value
                if not isinstance(val, str):
                    continue
                m = _ISO_DATE_ONLY.match(val)
                if not m:
                    continue
                y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
                try:
                    parsed = date(y, mo, d)
                except ValueError:
                    continue
                cell.value = parsed
                cell.number_format = DATE_DISPLAY_FORMAT
