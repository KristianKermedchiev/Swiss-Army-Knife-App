from src.gui.tabs.base_tab import BaseTab

class GoalsTab(BaseTab):
    def __init__(self):
        # Initialize with the todos.json file and column names
        super().__init__(data_file="path/to/goals.json", tab_name="Goals", columns=["ID", "Description", "Due Date"])
