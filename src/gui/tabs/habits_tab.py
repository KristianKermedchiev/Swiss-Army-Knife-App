from src.gui.tabs.base_tab import BaseTab

class HabitsTab(BaseTab):
    def __init__(self):
        # Initialize with the todos.json file and column names
        super().__init__(data_file="path/to/habits.json", tab_name="Habits", columns=["ID", "Description", "Due Date"])
