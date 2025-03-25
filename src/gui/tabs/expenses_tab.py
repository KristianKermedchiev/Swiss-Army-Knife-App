from src.gui.tabs.base_tab import BaseTab

class ExpensesTab(BaseTab):
    def __init__(self):
        super().__init__(data_file="path/to/expenses.json", tab_name="Expenses", columns=["ID", "Description", "Due Date"])
