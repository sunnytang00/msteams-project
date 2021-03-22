from src.data.data import data
from src.config import data_path
import json
from src.config import data_path

'''
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
            json.dump(data, f)
        return rv
    return wrapper
'''

def get_user() -> list:
    """Get list of user from data storage
    
    Arguments:
        This function takes no argument

    Returns:
        users (list): List of users
    """
    with open(data_path, 'r') as f:
        data = json.load(f)

    users = data['users']

    return users

def get_channel() -> list:
    """Get list of channel from data storage
    
    Arguments:
        This function takes no argument

    Returns:
        channels (list): List of channels
    """

    with open(data_path, 'r') as f:
        data = json.load(f)

    channels = data["channels"]
    return channels

def get_data() -> dict:
    """Get data stored on data storage
    
    Arguments:
        This function takes no argument

    Returns:
        data (dict): data stored on the data storage
    """
    with open(data_path, 'r') as f:
        data = json.load(f)

    return data

def store_user(user: dict) -> bool:
    """Store the data of user on data storage
    
    Arguments:
        user (list): List of users

    Returns:
        True if the user data stored successfully
        False if fail to store user data
    """
    data = get_data()
    
    data["users"] = user

    with open(data_path, 'w') as f:
        json.dump(data, f)

    if get_user() == data["users"]:
        return True
    return False

def store_channel(channel: list) -> bool:
    """Store the data of channel on data storage
    
    Arguments:
        channel (list): List of channel

    Returns:
        True if the channel data stored successfully
        False if fail to store channel data
    """
    data = get_data()

    data["channels"] = channel

    with open(data_path, 'w') as f:
        json.dump(data, f)

    if get_channel() == data["channels"]:
        return True
    return False
