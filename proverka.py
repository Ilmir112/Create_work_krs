import sys
from PyQt5.QtWidgets import QApplication, QTableWidget

app = QApplication(sys.argv)
table = QTableWidget()
table.setRowCount(10)
table.setColumnCount(10)
table.setStyleSheet("QTableView::item {background-color: black; color: white;}")
table.show()
sys.exit(app.exec_())