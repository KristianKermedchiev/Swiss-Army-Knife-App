from src.gui.tabs.base_tab import BaseTab
from PyQt5.QtWidgets import QComboBox, QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QPushButton, QWidget, QSizePolicy
from src.commands.habits import HABITS_DATA_FILE
from src.db.db_interface import load_data
from src.utils.file_utils import get_data_file_path
from datetime import datetime

HABITS_DATA_FILE = get_data_file_path('habits.json')

class HabitsTab(BaseTab):
    def __init__(self):
        super().__init__(tab_name="Habits")

        self.filter_layout = QHBoxLayout()

        filter_widget = QWidget()
        filter_widget.setLayout(self.filter_layout)
        filter_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(filter_widget)

        self.data_table = QTableWidget()
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.data_table)

        self.apply_styles()
        self.list_data()

        self.data_table.cellClicked.connect(self.on_habit_click)

    def list_data(self):
        habits = load_data(HABITS_DATA_FILE)

        filtered_habits = self.filter_data(habits)

        self.data_table.setRowCount(len(filtered_habits))
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["ID", "Name", "Goal", "Unit"])

        self.data_table.verticalHeader().setVisible(False)

        for row, habit in enumerate(filtered_habits):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(habit.get("id", ""))))
            self.data_table.setItem(row, 1, QTableWidgetItem(habit.get("name", "")))
            self.data_table.setItem(row, 2, QTableWidgetItem(habit.get("goal", "")))
            self.data_table.setItem(row, 3, QTableWidgetItem(habit.get("unit", "")))

        self.data_table.resizeColumnsToContents()

        header = self.data_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def on_habit_click(self, row, column):
        habit_id = int(self.data_table.item(row, 0).text())
        habit_name = self.data_table.item(row, 1).text()

        habits = load_data(HABITS_DATA_FILE)
        habit = next(h for h in habits if h["id"] == habit_id)

        self.open_log_dialog(habit)

    def open_log_dialog(self, habit):
        log_dialog = LogDialog(habit)
        log_dialog.exec_()

    def filter_data(self, habits):
        """Filters the habits if needed."""
        return habits

    def apply_styles(self):
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


class LogDialog(QDialog):
    def __init__(self, habit):
        super().__init__()

        self.habit = habit
        self.setWindowTitle(f"{habit['name']} - Log")

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setFixedSize(700, 600)

        layout = QVBoxLayout()

        self.year_combo = QComboBox()
        self.month_combo = QComboBox()

        self.populate_filters()

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.year_combo)
        filter_layout.addWidget(self.month_combo)

        layout.addLayout(filter_layout)

        self.log_table = QTableWidget()
        layout.addWidget(self.log_table)

        self.log_table.verticalHeader().setVisible(False)

        self.apply_styles()
        self.load_log_data()
        self.setLayout(layout)

    def populate_filters(self):
        current_date = datetime.now()
        current_year = str(current_date.year)
        current_month = current_date.strftime("%B")

        self.years = [2025, 2024, 2023]
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                       "November", "December"]

        self.year_combo.addItems([str(year) for year in self.years])
        self.month_combo.addItems(self.months)

        self.year_combo.setCurrentText(current_year)
        self.month_combo.setCurrentText(current_month)

        self.year_combo.currentIndexChanged.connect(self.filter_logs)
        self.month_combo.currentIndexChanged.connect(self.filter_logs)

    def load_log_data(self):
        logs = self.habit["log"]

        self.log_table.setRowCount(len(logs))
        self.log_table.setColumnCount(2)
        self.log_table.setHorizontalHeaderLabels(["Date", "Status"])

        for row, log in enumerate(logs):
            self.log_table.setItem(row, 0, QTableWidgetItem(log["date"]))
            self.log_table.setItem(row, 1, QTableWidgetItem(log["completed"]))

        self.log_table.resizeColumnsToContents()

        header = self.log_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def filter_logs(self):
        selected_year = self.year_combo.currentText()
        selected_month = self.month_combo.currentText()

        try:
            month_num = self.months.index(selected_month) + 1
            formatted_month = f"{month_num:02d}"

            filtered_logs = []
            for log in self.habit["log"]:
                day, month, year = log["date"].split("/")
                if month == formatted_month and year == selected_year:
                    filtered_logs.append(log)

            self.log_table.setRowCount(len(filtered_logs))

            for row, log in enumerate(filtered_logs):
                self.log_table.setItem(row, 0, QTableWidgetItem(log["date"]))
                self.log_table.setItem(row, 1, QTableWidgetItem(log["completed"]))

            self.log_table.resizeColumnsToContents()

            header = self.log_table.horizontalHeader()
            header.setStretchLastSection(True)
            header.setSectionResizeMode(QHeaderView.Stretch)

        except Exception as e:
            print(f"Error in filter_logs: {e}")
            return

    def apply_styles(self):
        self.year_combo.setStyleSheet("""
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

        self.month_combo.setStyleSheet("""
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

        self.log_table.setStyleSheet("""
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

        self.log_table.horizontalHeader().setStyleSheet("""
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

        self.log_table.horizontalHeader().setStretchLastSection(True)
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
