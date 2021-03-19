from src.data.data import data
from src.config import data_path
from json import dump

def get_data():
    global data
    return data

def save_data(func):
    """Save data to json file."""
    def wrapper(*args, **kwargs):
        rv = func(*args, **kwargs)
        # if no exceptions are raised
        data = get_data()
        with open(data_path, 'w') as f:
            dump(data, f)
        return rv
    return wrapper
