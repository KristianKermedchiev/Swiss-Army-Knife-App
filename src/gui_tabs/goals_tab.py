from gui_tabs.base_tab import BaseTab
from PyQt5.QtWidgets import QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QSizePolicy, QWidget
from db.db_interface import load_data
from utils.file_utils import get_data_file_path

GOALS_DATA_FILE = get_data_file_path('goals.json')

class GoalsTab(BaseTab):
    def __init__(self):
        super().__init__(tab_name="Goals")

        self.filter_layout = QHBoxLayout()

        self.archived_combo = QComboBox()
        self.archived_combo.addItems(
            ["All", "Archived", "Active"])
        self.archived_combo.setCurrentText("All")
        self.filter_layout.addWidget(self.archived_combo)

        self.status_combo = QComboBox()
        self.status_combo.addItems(
            ["All", "In Progress", "Completed"])
        self.status_combo.setCurrentText("All")
        self.filter_layout.addWidget(self.status_combo)

        self.list_button = QPushButton("List Goals")
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
        goals = load_data(GOALS_DATA_FILE)

        selected_archived = self.archived_combo.currentText()
        selected_status = self.status_combo.currentText()

        filtered_goals = self.filter_data(goals, selected_archived, selected_status)

        self.data_table.setRowCount(len(filtered_goals))
        self.data_table.setColumnCount(9)
        self.data_table.setHorizontalHeaderLabels(["ID", "Name", "Unit", "Start", "End", "Status", "Progress", "Category", "Archived"])

        self.data_table.verticalHeader().setVisible(False)

        for row, goal in enumerate(filtered_goals):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(goal.get("id", ""))))
            self.data_table.setItem(row, 1, QTableWidgetItem(goal.get("name", "")))
            self.data_table.setItem(row, 2, QTableWidgetItem(goal.get("unit", "")))
            self.data_table.setItem(row, 3, QTableWidgetItem(goal.get("startingValue", "")))
            self.data_table.setItem(row, 4, QTableWidgetItem(goal.get("endValue", "")))
            self.data_table.setItem(row, 5, QTableWidgetItem(goal.get("status", "")))
            progress_value = goal.get("progress", "")
            progress_text = f"{progress_value}%" if progress_value else ""
            self.data_table.setItem(row, 6, QTableWidgetItem(progress_text))
            self.data_table.setItem(row, 7, QTableWidgetItem(goal.get("category", "")))

            archived_status = "Archived" if goal.get("archived", False) else "Active"
            self.data_table.setItem(row, 8, QTableWidgetItem(archived_status))

        self.data_table.resizeColumnsToContents()

        header = self.data_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def filter_data(self, goals, selected_archived, selected_status):
        """Filters the goals based on selected archived status and goal status."""
        filtered = []

        if selected_archived != "All":
            if selected_archived == "Archived":
                goals = [goal for goal in goals if goal.get("archived", False) == True]
            elif selected_archived == "Active":
                goals = [goal for goal in goals if goal.get("archived", False) == False]

        if selected_status != "All":
            filtered = [
                goal for goal in goals if goal.get("status") == selected_status
            ]
        else:
            filtered = goals

        return filtered

    def apply_styles(self):
        """Applies enhanced custom styles to widgets with dynamic width."""
        self.archived_combo.setStyleSheet("""
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

        self.status_combo.setStyleSheet("""
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