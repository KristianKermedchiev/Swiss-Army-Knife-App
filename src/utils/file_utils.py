import os
import sys

def get_data_file_path(filename):
    """Returns the correct path for a JSON file, ensuring it is stored in the .exe directory."""
    if getattr(sys, 'frozen', False):  # Running as .exe
        base_dir = os.path.dirname(sys.executable)  # Get .exe location
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script location

    return os.path.join(base_dir, filename)
