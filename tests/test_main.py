import pytest
from PyQt5 import QtCore, QtTest, QtWidgets

from main import MyWindow


@pytest.fixture
def main_window():
    window = MyWindow()
    window.show()
    yield window
    window.close()

def test_main_window_opens(main_window):
    assert main_window.isVisible()

def test_data_entry(main_window):
    # Ввести текст в поле ввода
    main_window.line_edit.setText("Hello World")

    # Проверить введенный текст
    assert main_window.line_edit.text() == "Hello World"

    # Выбрать элемент в раскрывающемся списке
    main_window.combo_box.setCurrentText("Item 2")

    # Проверить выбранный элемент
    assert main_window.combo_box.currentText() == "Item 2"


