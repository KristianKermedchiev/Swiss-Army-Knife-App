from src.gui_tabs.base_tab import BaseTab
from PyQt5.QtWidgets import (QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QHBoxLayout, QHeaderView, QSizePolicy, QWidget, QVBoxLayout,
                             QDialog, QLabel, QGroupBox, QGridLayout, QFrame)
from PyQt5.QtCore import Qt
from src.db.db_interface import load_data
from src.utils.file_utils import get_data_file_path
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from collections import defaultdict

EXPENSES_DATA_FILE = get_data_file_path('expenses.json')


class ExpensesTab(BaseTab):
    def __init__(self):
        super().__init__(tab_name="Bills")

        self.filter_layout = QHBoxLayout()

        current_year = str(datetime.now().year)
        self.year_combo = QComboBox()
        self.year_combo.addItem("All")
        for year in range(2025, 2030):
            self.year_combo.addItem(str(year))
        self.year_combo.setCurrentText(current_year)
        self.filter_layout.addWidget(self.year_combo)

        current_month = datetime.now().strftime("%B")
        self.month_combo = QComboBox()
        self.month_combo.addItems(
            ["All", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"])
        self.month_combo.setCurrentText(current_month)
        self.filter_layout.addWidget(self.month_combo)

        self.list_button = QPushButton("List Expenses")
        self.list_button.clicked.connect(self.list_data)
        self.filter_layout.addWidget(self.list_button)

        self.report_button = QPushButton("Get Month Report")
        self.report_button.clicked.connect(self.show_month_report)
        self.filter_layout.addWidget(self.report_button)

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
        expenses = load_data(EXPENSES_DATA_FILE)

        selected_year = self.year_combo.currentText()
        selected_month = self.month_combo.currentText()

        filtered_bills = self.filter_data(expenses, selected_year, selected_month)

        self.data_table.setRowCount(len(filtered_bills))
        self.data_table.setColumnCount(5)  # Updated to 5 columns to include Category
        self.data_table.setHorizontalHeaderLabels(["ID", "Date", "Description", "Amount", "Category"])

        self.data_table.verticalHeader().setVisible(False)

        for row, bill in enumerate(filtered_bills):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(bill.get("id", ""))))
            self.data_table.setItem(row, 1, QTableWidgetItem(bill.get("date", "")))
            self.data_table.setItem(row, 2, QTableWidgetItem(bill.get("description", "")))
            self.data_table.setItem(row, 3, QTableWidgetItem(str(bill.get("amount", ""))))
            self.data_table.setItem(row, 4, QTableWidgetItem(bill.get("category", "")))

        self.data_table.resizeColumnsToContents()

        header = self.data_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def filter_data(self, expenses, selected_year, selected_month):
        """Filters the bills based on selected year and month."""
        filtered = []

        if selected_year != "All":
            expenses = [expense for expense in expenses if expense.get("date", "").endswith(selected_year)]

        if selected_month != "All":
            filtered = [
                expense for expense in expenses if self.get_month_name_from_date(expense.get("date")) == selected_month
            ]
        else:
            filtered = expenses

        return filtered

    def get_month_name_from_date(self, date_string):
        """Extract the month name from a date string (dd/mm/yyyy)."""
        try:
            date_obj = datetime.strptime(date_string, "%d/%m/%Y")
            return date_obj.strftime("%B")
        except ValueError:
            return ""

    def prepare_data_for_visualization(self, expenses):
        """Prepares expense data for visualization."""
        # Standardize amount formatting (handle comma as decimal separator)
        for expense in expenses:
            if isinstance(expense.get("amount"), str):
                expense["amount"] = float(expense.get("amount", "0").replace(",", "."))

        # Group expenses by category
        category_data = defaultdict(float)
        for expense in expenses:
            category = expense.get("category", "Uncategorized")
            amount = expense.get("amount", 0)
            category_data[category] += float(amount)

        return category_data

    def get_monthly_totals(self, expenses):
        """Get total expenses by date within a month."""
        date_totals = defaultdict(float)
        for expense in expenses:
            date = expense.get("date", "")
            if date:
                try:
                    date_obj = datetime.strptime(date, "%d/%m/%Y")
                    day = date_obj.day
                    amount = float(str(expense.get("amount", "0")).replace(",", "."))
                    date_totals[day] += amount
                except (ValueError, TypeError):
                    continue
        return date_totals

    def show_month_report(self):
        """Shows a comprehensive monthly expense report with visualizations."""
        expenses = load_data(EXPENSES_DATA_FILE)

        selected_year = self.year_combo.currentText()
        selected_month = self.month_combo.currentText()

        # Create a dialog to show the report
        report_dialog = QDialog()
        report_dialog.setWindowTitle(f"Expense Report: {selected_month} {selected_year}")
        report_dialog.setMinimumSize(1200, 900)

        # Main layout
        main_layout = QVBoxLayout(report_dialog)

        # Header
        header_label = QLabel(f"<h1>Expense Report: {selected_month} {selected_year}</h1>")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Stats summary section
        stats_group = QGroupBox("Summary Statistics")
        stats_layout = QGridLayout()
        stats_group.setLayout(stats_layout)

        # Filter data for current month
        current_month_data = self.filter_data(expenses, selected_year, selected_month)

        # If no data available
        if not current_month_data:
            main_layout.addWidget(QLabel("No expense data available for the selected period."))
            report_dialog.exec_()
            return

        # Calculate stats
        total_expenses = sum(float(str(expense.get("amount", "0")).replace(",", "."))
                             for expense in current_month_data)
        avg_expense = total_expenses / len(current_month_data) if current_month_data else 0
        category_counts = len(set(expense.get("category", "") for expense in current_month_data))

        # Add stats to layout
        stats_layout.addWidget(QLabel("<b>Total Expenses:</b>"), 0, 0)
        stats_layout.addWidget(QLabel(f"{total_expenses:.2f}"), 0, 1)
        stats_layout.addWidget(QLabel("<b>Number of Transactions:</b>"), 1, 0)
        stats_layout.addWidget(QLabel(f"{len(current_month_data)}"), 1, 1)

        stats_layout.addWidget(QLabel("<b>Average Expense:</b>"), 2, 0)
        stats_layout.addWidget(QLabel(f"{avg_expense:.2f}"), 2, 1)

        stats_layout.addWidget(QLabel("<b>Categories:</b>"), 3, 0)
        stats_layout.addWidget(QLabel(f"{category_counts}"), 3, 1)

        main_layout.addWidget(stats_group)

        # Charts section
        charts_group = QGroupBox("Expense Visualizations")
        charts_layout = QGridLayout()
        charts_group.setLayout(charts_layout)

        # Prepare data for charts
        category_data = self.prepare_data_for_visualization(current_month_data)
        daily_totals = self.get_monthly_totals(current_month_data)

        # Create Category Pie Chart
        pie_figure = Figure(figsize=(4, 4))
        pie_canvas = FigureCanvas(pie_figure)
        pie_ax = pie_figure.add_subplot(111)

        categories = list(category_data.keys())
        amounts = list(category_data.values())

        if categories:
            pie_ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
            pie_ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            pie_ax.set_title('Expenses by Category')

        # Create Daily Expense Bar Chart
        bar_figure = Figure(figsize=(5, 4))
        bar_canvas = FigureCanvas(bar_figure)
        bar_ax = bar_figure.add_subplot(111)

        days = sorted(daily_totals.keys())
        day_amounts = [daily_totals[day] for day in days]

        if days:
            bar_ax.bar(days, day_amounts)
            bar_ax.set_xlabel('Day of Month')
            bar_ax.set_ylabel('Amount')
            bar_ax.set_title('Daily Expenses')

        # Add comparison option
        comparison_group = QGroupBox("Month Comparison")
        comparison_layout = QVBoxLayout()
        comparison_group.setLayout(comparison_layout)

        comparison_header = QHBoxLayout()
        comparison_layout.addLayout(comparison_header)

        comparison_label = QLabel("Compare with month:")
        comparison_header.addWidget(comparison_label)

        comparison_combo = QComboBox()
        comparison_combo.addItems(["January", "February", "March", "April", "May", "June",
                                   "July", "August", "September", "October", "November", "December"])

        # Set a different month for comparison
        current_month_idx = comparison_combo.findText(selected_month)
        comparison_month_idx = (current_month_idx - 1) % 12  # Previous month by default
        comparison_combo.setCurrentIndex(comparison_month_idx)

        comparison_header.addWidget(comparison_combo)

        comparison_button = QPushButton("Compare")
        comparison_header.addWidget(comparison_button)

        # Create container for comparison chart
        comparison_chart_container = QFrame()
        comparison_chart_layout = QVBoxLayout(comparison_chart_container)
        comparison_layout.addWidget(comparison_chart_container)

        # Function to update comparison chart
        def update_comparison():
            # Clear previous chart
            for i in reversed(range(comparison_chart_layout.count())):
                comparison_chart_layout.itemAt(i).widget().setParent(None)

            comparison_month = comparison_combo.currentText()

            # Get data for comparison month
            comparison_data = self.filter_data(expenses, selected_year, comparison_month)

            if not comparison_data:
                comparison_chart_layout.addWidget(QLabel(f"No data available for {comparison_month} {selected_year}"))
                return

            # Prepare data for comparison
            current_categories = self.prepare_data_for_visualization(current_month_data)
            comparison_categories = self.prepare_data_for_visualization(comparison_data)

            # Get all unique categories
            all_categories = sorted(set(list(current_categories.keys()) + list(comparison_categories.keys())))

            # Create comparison chart
            comparison_figure = Figure(figsize=(8, 5))
            comparison_canvas = FigureCanvas(comparison_figure)
            comparison_ax = comparison_figure.add_subplot(111)

            x = np.arange(len(all_categories))
            width = 0.35

            current_amounts = [current_categories.get(cat, 0) for cat in all_categories]
            comparison_amounts = [comparison_categories.get(cat, 0) for cat in all_categories]

            comparison_ax.bar(x - width / 2, current_amounts, width, label=selected_month)
            comparison_ax.bar(x + width / 2, comparison_amounts, width, label=comparison_month)

            comparison_ax.set_xticks(x)
            comparison_ax.set_xticklabels(all_categories)
            plt.setp(comparison_ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

            comparison_ax.set_ylabel('Amount')
            comparison_ax.set_title(f'Category Comparison: {selected_month} vs {comparison_month}')
            comparison_ax.legend()

            comparison_figure.tight_layout()

            comparison_chart_layout.addWidget(comparison_canvas)

            # Add stats comparison
            comparison_total = sum(comparison_amounts)
            current_total = sum(current_amounts)

            diff_percentage = ((current_total - comparison_total) / comparison_total * 100) if comparison_total else 0

            stats_label = QLabel(
                f"<b>Comparison Summary:</b> Total spending in {selected_month}: {current_total:.2f} | "
                f"Total spending in {comparison_month}: {comparison_total:.2f} | "
                f"Change: {diff_percentage:+.2f}%")

            comparison_chart_layout.addWidget(stats_label)

        # Connect comparison button
        comparison_button.clicked.connect(update_comparison)

        # Add the charts to the layout
        charts_layout.addWidget(pie_canvas, 0, 0)
        charts_layout.addWidget(bar_canvas, 0, 1)

        # Add everything to main layout
        main_layout.addWidget(charts_group)
        main_layout.addWidget(comparison_group)

        # Update comparison initially
        update_comparison()

        # Show the dialog
        report_dialog.exec_()

    def apply_styles(self):
        """Applies enhanced custom styles to widgets with dynamic width."""
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

        self.report_button.setStyleSheet("""
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