from src.gui.tabs.base_tab import BaseTab
from PyQt5.QtWidgets import QComboBox, QDialog, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QWidget, QSizePolicy
from src.db.db_interface import load_data
from src.utils.file_utils import get_data_file_path

STUDIES_DATA_FILE = get_data_file_path('studies.json')

class StudiesTab(BaseTab):
    def __init__(self):
        super().__init__(tab_name="Studies")

        self.filter_layout = QHBoxLayout()

        filter_widget = QWidget()
        filter_widget.setLayout(self.filter_layout)
        filter_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.status = QComboBox()
        self.status.addItems(
            ["All", "In Progress", "Completed"])
        self.status.setCurrentText("All")
        self.filter_layout.addWidget(self.status)

        self.category = QComboBox()
        self.category.addItems(self.get_unique_categories())
        self.category.setCurrentText("All")
        self.filter_layout.addWidget(self.category)

        self.list_button = QPushButton("List Studies")
        self.list_button.clicked.connect(self.list_data)
        self.filter_layout.addWidget(self.list_button)

        self.layout.addWidget(filter_widget)

        self.data_table = QTableWidget()
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.data_table)

        self.apply_styles()
        self.list_data()

        self.data_table.cellClicked.connect(self.on_study_click)

    def get_unique_categories(self):
        """Fetches unique categories from the dataset."""
        studies = load_data(STUDIES_DATA_FILE)
        categories = {study['category'] for study in studies}
        return ["All"] + sorted(categories)

    def list_data(self):
        studies = load_data(STUDIES_DATA_FILE)

        self.data_table.setRowCount(len(studies))
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Status"])

        self.data_table.verticalHeader().setVisible(False)

        for row, study in enumerate(studies):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(study.get("id", ""))))
            self.data_table.setItem(row, 1, QTableWidgetItem(study.get("name", "")))
            self.data_table.setItem(row, 2, QTableWidgetItem(study.get("category", "")))
            self.data_table.setItem(row, 3, QTableWidgetItem(study.get("status", "")))

        self.data_table.resizeColumnsToContents()

        header = self.data_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def on_study_click(self, row, column):
        study_id = int(self.data_table.item(row, 0).text())
        studies = load_data(STUDIES_DATA_FILE)

        study = next((s for s in studies if s["id"] == study_id), None)
        if study is None:
            print(f"Study with ID {study_id} not found")
            return

        self.open_log_dialog(study)

    def open_log_dialog(self, study):
        log_dialog = LogDialog(study)
        log_dialog.exec_()

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
    def __init__(self, study):
        super().__init__()

        self.study = study
        self.setWindowTitle(f"{study['name']} - Topics Log")

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setFixedSize(700, 600)

        layout = QVBoxLayout()

        self.topic_table = QTableWidget()
        layout.addWidget(self.topic_table)

        self.topic_table.verticalHeader().setVisible(False)

        self.apply_styles()
        self.load_log_data()
        self.setLayout(layout)

    def load_log_data(self):
        topics = self.study["topics"]

        self.topic_table.setRowCount(len(topics))
        self.topic_table.setColumnCount(2)
        self.topic_table.setHorizontalHeaderLabels(["Date", "Topic"])

        for row, topic in enumerate(topics):
            self.topic_table.setItem(row, 0, QTableWidgetItem(topic["date"]))
            self.topic_table.setItem(row, 1, QTableWidgetItem(topic["name"]))

        self.topic_table.resizeColumnsToContents()

        header = self.topic_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def apply_styles(self):
        self.topic_table.setStyleSheet("""
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

        self.topic_table.horizontalHeader().setStyleSheet("""
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

        self.topic_table.horizontalHeader().setStretchLastSection(True)
        self.topic_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
