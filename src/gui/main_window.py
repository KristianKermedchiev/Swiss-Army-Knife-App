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

        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Create a tab widget to hold the tabs
        self.tab_widget = QTabWidget()

        # Add the different modules as tabs
        self.bills_tab = BillsTab()
        self.tab_widget.addTab(self.bills_tab, "Bills")

        self.expenses_tab = ExpensesTab()
        self.tab_widget.addTab(self.expenses_tab, "Expenses")

        self.goals_tab = GoalsTab()
        self.tab_widget.addTab(self.goals_tab, "Goals")

        self.habits_tab = HabitsTab()
        self.tab_widget.addTab(self.habits_tab, "Habits")

        self.books_tab = BooksTab()
        self.tab_widget.addTab(self.books_tab, "Books")

        self.studies_tab = StudiesTab()
        self.tab_widget.addTab(self.studies_tab, "Studies")

        self.todos_tab = TodosTab()
        self.tab_widget.addTab(self.todos_tab, "Todos")

        self.setCentralWidget(self.tab_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
