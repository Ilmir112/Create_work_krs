from PyQt5.QtWidgets import QDialog, QVBoxLayout

class ModalDialog(QDialog):
    def __init__(self, window, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(window)

        self.setLayout(layout)



