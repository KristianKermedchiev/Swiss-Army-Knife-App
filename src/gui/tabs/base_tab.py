from PyQt5.QtWidgets import QWidget, QVBoxLayout

class BaseTab(QWidget):
    def __init__(self, tab_name):
        super().__init__()

        self.tab_name = tab_name
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)


