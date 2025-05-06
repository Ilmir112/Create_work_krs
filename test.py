from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QLabel
import requests
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.well_input = QLineEdit(self)
        self.area_input = QLineEdit(self)
        self.result_label = QLabel(self)

        btn = QPushButton("Найти скважину", self)
        btn.clicked.connect(self.search_well)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Номер скважины:"))
        layout.addWidget(self.well_input)
        layout.addWidget(QLabel("Область месторождения:"))
        layout.addWidget(self.area_input)
        layout.addWidget(btn)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle("Поиск скважины без глушения")
        self.show()

    def search_well(self):
        well_number = self.well_input.text()
        deposit_area = self.area_input.text()

        result = self.get_well_silencing(well_number, deposit_area)
        if result:
            self.result_label.setText(str(result))
        else:
            self.result_label.setText("Результат не найден или произошла ошибка.")

    def get_well_silencing(self, well_number, deposit_area):

        api_url = 'http://localhost:8000/wells_silencing_router/add_data_well_silencing'
        try:
            data = {
                "well_number": f'{well_number}',
                "deposit_area": deposit_area,
                "today": "2025-05-04",
                "region": "ТГМ",
                "costumer": "БНД"
            }

            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: статус код {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Запрос не удался: {e}")
            return None

app = QApplication([])
window = MyApp()
app.exec_()
