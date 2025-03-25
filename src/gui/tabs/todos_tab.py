from src.gui.tabs.base_tab import BaseTab

class TodosTab(BaseTab):
    def __init__(self):
        # Initialize with the todos.json file and column names
        super().__init__(data_file="path/to/todos.json", tab_name="Todos", columns=["ID", "Description", "Due Date"])
