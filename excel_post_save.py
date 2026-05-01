# -*- coding: utf-8 -*-
"""Действия после сохранения openpyxl: снять read-only с файла, открыть книгу в Excel для редактирования."""
import win32api
import win32con


def ensure_excel_file_writable_on_disk(path):
    """Снять системный атрибут FILE_ATTRIBUTE_READONLY, если он стоит на файле."""
    try:
        attrs = win32api.GetFileAttributes(path)
        if attrs == -1:
            return
        if attrs & win32con.FILE_ATTRIBUTE_READONLY:
            win32api.SetFileAttributes(path, attrs & ~win32con.FILE_ATTRIBUTE_READONLY)
    except Exception:
        pass


def com_open_workbook_editable(excel_app, path):
    """
    Открыть книгу не в режиме «только чтение» и игнорировать «рекомендуется только чтение» в свойствах книги.
    """
    try:
        return excel_app.Workbooks.Open(
            Filename=path,
            UpdateLinks=0,
            ReadOnly=False,
            IgnoreReadOnlyRecommended=True,
            Editable=True,
        )
    except TypeError:
        # Старые сборки Excel / pywin32 без части именованных аргументов
        return excel_app.Workbooks.Open(path, 0, False)
