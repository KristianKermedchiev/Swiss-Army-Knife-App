from src.gui_tabs.base_tab import BaseTab
from PyQt5.QtWidgets import QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QSizePolicy, QWidget
from src.db.db_interface import load_data
from src.utils.file_utils import get_data_file_path

TODO_DATA_FILE = get_data_file_path('todos.json')


class TodosTab(BaseTab):
    def __init__(self):
        super().__init__(tab_name="Todos")

        self.filter_layout = QHBoxLayout()

        self.category_combo = QComboBox()
        self.category_combo.addItems(["all", "incomplete", "complete"])
        self.category_combo.setCurrentText("incomplete")
        self.filter_layout.addWidget(self.category_combo)

        self.list_button = QPushButton("List Todos")
        self.list_button.clicked.connect(self.list_data)
        self.filter_layout.addWidget(self.list_button)

        filter_widget = QWidget()
        filter_widget.setLayout(self.filter_layout)
        filter_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(filter_widget)

        self.data_table = QTableWidget()
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.data_table)

        self.apply_styles()
        self.list_data()

    def list_data(self):
        todos = load_data(TODO_DATA_FILE)

        selected_category = self.category_combo.currentText()

        filtered_todos = self.filter_data(todos, selected_category)

        self.data_table.setRowCount(len(filtered_todos))
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["ID", "Description", "Due Date", "Status"])

        self.data_table.verticalHeader().setVisible(False)

        for row, todo in enumerate(filtered_todos):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(todo.get("id", ""))))
            self.data_table.setItem(row, 1, QTableWidgetItem(todo.get("description", "")))
            self.data_table.setItem(row, 2, QTableWidgetItem(todo.get("due_date", "")))
            self.data_table.setItem(row, 3, QTableWidgetItem(todo.get("status", "")))

        self.data_table.resizeColumnsToContents()

        header = self.data_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def filter_data(self, todos, selected_category):
        """Filters the todos based on category."""
        filtered = []

        for todo in todos:
            if selected_category == "all":
                filtered.append(todo)
            elif selected_category == "incomplete" and todo.get("status") == "incomplete":
                filtered.append(todo)
            elif selected_category == "complete" and todo.get("status") == "complete":
                filtered.append(todo)

        return filtered

    def apply_styles(self):
        """Applies enhanced custom styles to widgets with dynamic width."""
        self.category_combo.setStyleSheet("""
            QComboBox {
                font-size: 16px;
                padding: 8px 12px;
                background-color: #ffffff;
                border: 2px solid #e1e4e8;
                border-radius: 6px;
                color: #2c3e50;
                selection-background-color: #3498db;
            }

            QComboBox:hover {
                border-color: #3498db;
                transition: border-color 0.3s ease;
            }
        """)

        self.list_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: 600;
                padding: 8px 15px;
                border-radius: 6px;
                border: none;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.1s ease;
            }

            QPushButton:hover {
                background-color: #2980b9;
                transform: scale(1.05);
            }

            QPushButton:pressed {
                background-color: #21618c;
                transform: scale(0.95);
            }
        """)

        self.data_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 8px;
                gridline-color: #f1f3f5;
                font-size: 14px;
                color: #2c3e50;
                margin: 0 auto;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f1f3f5;
                background-color: #ffffff;
                transition: background-color 0.2s ease;
            }

            QTableWidget::item:selected {
                background-color: #e6f2ff;
                color: #2c3e50;
            }

            QTableWidget::item:hover {
                background-color: #f7f9fc;
            }
        """)

        self.data_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-weight: 600;
                border: none;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            QHeaderView::section:horizontal {
                border-bottom: 3px solid #2980b9;
            }
        """)

        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
