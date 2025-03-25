from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from src.db.db_interface import load_data

class BaseTab(QWidget):
    def __init__(self, data_file, tab_name, columns):
        super().__init__()

        self.data_file = data_file
        self.tab_name = tab_name
        self.columns = columns

        self.layout = QVBoxLayout()

        # Add category filter
        self.category_combo = QComboBox()
        self.category_combo.addItems(["All"])
        self.layout.addWidget(self.category_combo)

        # Add date range filter
        self.start_date_picker = QDateEdit()
        self.start_date_picker.setCalendarPopup(True)
        self.layout.addWidget(self.start_date_picker)

        self.end_date_picker = QDateEdit()
        self.end_date_picker.setCalendarPopup(True)
        self.layout.addWidget(self.end_date_picker)

        # Add button to list data
        self.list_button = QPushButton(f"List {self.tab_name}")
        self.list_button.clicked.connect(self.list_data)
        self.layout.addWidget(self.list_button)

        # Table to display data
        self.data_table = QTableWidget()
        self.layout.addWidget(self.data_table)

        self.setLayout(self.layout)

        # Apply styles to widgets
        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
                border-radius: 10px;
            }
            QComboBox {
                padding: 8px;
                background-color: #e0e0e0;
                border-radius: 5px;
            }
            QDateEdit {
                padding: 8px;
                background-color: #e0e0e0;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTableWidget {
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                gridline-color: #f0f0f0;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::horizontalHeader {
                background-color: #f2f2f2;
                font-weight: bold;
            }
        """)

    def list_data(self):
        data = load_data(self.data_file)
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(self.columns))  # Set columns dynamically

        # Set column headers
        self.data_table.setHorizontalHeaderLabels(self.columns)

        for row, item in enumerate(data):
            for col, key in enumerate(self.columns):
                self.data_table.setItem(row, col, QTableWidgetItem(str(item.get(key, ""))))
