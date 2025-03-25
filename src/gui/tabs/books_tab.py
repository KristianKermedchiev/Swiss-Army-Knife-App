from src.gui.tabs.base_tab import BaseTab

class BooksTab(BaseTab):
    def __init__(self):
        super().__init__(data_file="path/to/books.json", tab_name="Books", columns=["ID", "Description", "Due Date"])
