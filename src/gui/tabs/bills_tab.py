from src.gui.tabs.base_tab import BaseTab

class BillsTab(BaseTab):
    def __init__(self):
        super().__init__(data_file="path/to/bills.json", tab_name="Bills", columns=["ID", "Description", "Due Date"])
