from src.gui.tabs.base_tab import BaseTab
from PyQt5.QtWidgets import QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QSizePolicy, QWidget
from src.db.db_interface import load_data
from src.utils.file_utils import get_data_file_path
from datetime import datetime

BOOKS_DATA_FILE = get_data_file_path('books.json')

class BooksTab(BaseTab):
    def __init__(self):
        super().__init__(tab_name="Books")

        self.filter_layout = QHBoxLayout()

        self.genre_combo = QComboBox()
        self.genre_combo.addItem("All")
        self.genre_combo.addItem("Horror")
        self.genre_combo.addItem("Fantasy")
        self.genre_combo.addItem("Sci-Fi")
        self.genre_combo.setCurrentText("All")
        self.filter_layout.addWidget(self.genre_combo)

        self.status = QComboBox()
        self.status.addItems(
            ["All", "In Progress", "Completed"])
        self.status.setCurrentText("All")
        self.filter_layout.addWidget(self.status)

        self.list_button = QPushButton("List Books")
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
        books = load_data(BOOKS_DATA_FILE)

        selected_genre = self.genre_combo.currentText()
        selected_status = self.status.currentText()

        filtered_books = self.filter_data(books, selected_genre, selected_status)

        self.data_table.setRowCount(len(filtered_books))
        self.data_table.setColumnCount(8)
        self.data_table.setHorizontalHeaderLabels(["ID", "Title", "Genre", "Pages", "Pages Read", "Progress", "Status", "Rating"])

        self.data_table.verticalHeader().setVisible(False)

        for row, bill in enumerate(filtered_books):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(bill.get("id", ""))))
            self.data_table.setItem(row, 1, QTableWidgetItem(bill.get("title", "")))
            self.data_table.setItem(row, 2, QTableWidgetItem(bill.get("genre", "")))
            self.data_table.setItem(row, 3, QTableWidgetItem(bill.get("pages", "")))
            self.data_table.setItem(row, 4, QTableWidgetItem(str(bill.get("pages_read", 0))))
            self.data_table.setItem(row, 5, QTableWidgetItem(str(bill.get("progress", ""))))
            self.data_table.setItem(row, 6, QTableWidgetItem(bill.get("status", "")))
            self.data_table.setItem(row, 7, QTableWidgetItem(bill.get("rating", "")))

        self.data_table.resizeColumnsToContents()

        header = self.data_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def filter_data(self, books, selected_genre, selected_status):
        """Filters the books based on selected genre and status."""
        filtered = []

        if selected_genre != "All":
            books = [book for book in books if book.get("genre") == selected_genre]

        if selected_status != "All":
            books = [book for book in books if book.get("status") == selected_status]

        return books

    def apply_styles(self):
        """Applies enhanced custom styles to widgets with dynamic width."""
        self.genre_combo.setStyleSheet("""
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

        self.status.setStyleSheet("""
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



