from src.gui.tabs.base_tab import BaseTab

class StudiesTab(BaseTab):
    def __init__(self):
        # Initialize with the todos.json file and column names
        super().__init__(data_file="path/to/studies.json", tab_name="Studies", columns=["ID", "Description", "Due Date"])
