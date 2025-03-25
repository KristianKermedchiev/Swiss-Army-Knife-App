from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from src.gui.tabs.bills_tab import BillsTab
from src.gui.tabs.expenses_tab import ExpensesTab
from src.gui.tabs.goals_tab import GoalsTab
from src.gui.tabs.habits_tab import HabitsTab
from src.gui.tabs.books_tab import BooksTab
from src.gui.tabs.studies_tab import StudiesTab
from src.gui.tabs.todos_tab import TodosTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Swiss-Army-Knife-App-GUI")
        self.setGeometry(100, 100, 1000, 600)

        self.tab_widget = QTabWidget()

        self.bills_tab = BillsTab()
        self.tab_widget.addTab(self.bills_tab, "Bills")

        self.books_tab = BooksTab()
        self.tab_widget.addTab(self.books_tab, "Books")

        self.expenses_tab = ExpensesTab()
        self.tab_widget.addTab(self.expenses_tab, "Expenses")

        self.goals_tab = GoalsTab()
        self.tab_widget.addTab(self.goals_tab, "Goals")

        self.habits_tab = HabitsTab()
        self.tab_widget.addTab(self.habits_tab, "Habits")

        self.studies_tab = StudiesTab()
        self.tab_widget.addTab(self.studies_tab, "Studies")

        self.todos_tab = TodosTab()
        self.tab_widget.addTab(self.todos_tab, "Todos")

        # Set styling
        self.setStyleSheet("""
            /* Main Window Background */
            QMainWindow {
                background-color: #f0f4f8;
                font-family: 'Segoe UI', Roboto, Arial, sans-serif;
            }

            /* Tab Widget Pane */
            QTabWidget::pane {
                border: 1px solid #e1e4e8;
                border-radius: 10px;
                background-color: #ffffff;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            /* Tab Bar Styling */
            QTabBar::tab {
                background-color: #2c3e50;
                color: #ffffff;
                padding: 10px 15px;
                border-radius: 6px;
                margin: 5px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                min-width: 100px;
                transition: background-color 0.3s ease;
            }

            QTabBar::tab:hover {
                background-color: #34495e;
            }

            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }

            /* Tab Widget Overall */
            QTabWidget {
                background-color: transparent;
                border-radius: 10px;
            }

            /* Scrollable Tabs Styling */
            QTabBar::scroller {
                width: 20px;
            }

            QTabBar QToolButton {
                background-color: #f0f4f8;
                border: 1px solid #e1e4e8;
                border-radius: 4px;
            }

            QTabBar QToolButton::left-arrow {
                image: url(:/qt-project.org/styles/commonstyle/images/left-32.png);
            }

            QTabBar QToolButton::right-arrow {
                image: url(:/qt-project.org/styles/commonstyle/images/right-32.png);
            }
        """)

        self.setCentralWidget(self.tab_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()