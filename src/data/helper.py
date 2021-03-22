from src.config import data_path
import json

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

def clear_data() -> None:
    cleared_data = {
        "users": [],
        "channels": []
    }

    with open(data_path, 'w') as f:
        json.dump(cleared_data, f)

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


def get_users() -> list:
    """Get list of user from data storage
    
    Arguments:
        This function takes no argument

    Returns:
        users (list): List of users
    """
    # TODO: make getters one liners.
    data = get_data()

    users = data.get('users')

    return users

def get_channels() -> list:
    """Get list of channel from data storage
    
    Arguments:
        This function takes no argument

    Returns:
        channels (list): List of channels
    """
    data = get_data()

    channels = data.get("channels")
    return channels


def store_user(user: dict) -> bool:
    """store the data of user on data storage
    
    arguments:
        user (list): list of users

    returns:
        true if the user data stored successfully
        false if fail to store user data
    """
    data = get_data()
    
    data["users"].append(user)

    with open(data_path, 'w') as f:
        json.dump(data, f)

    if get_users() == data["users"]:
        return True
    return False

def update_name_first(u_id: int, name_first: str) -> bool:
    """TODO"""
    data = get_data()

    data["users"][u_id-1]["name_first"] = name_first

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_name_last(u_id: int, name_last: str) -> bool:
    """TODO"""
    data = get_data()

    data["users"][u_id-1]["name_last"] = name_last

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_email(u_id: int, email: str) -> bool:
    """TODO"""
    data = get_data()

    data["users"][u_id-1]["email"] = email

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_handle_str(u_id: int, handle_str: str) -> bool:
    """TODO"""
    data = get_data()

    data["users"][u_id-1]["handle_str"] = handle_str 

    with open(data_path, 'w') as f:
        json.dump(data, f)

def store_channel(channel: list) -> bool:
    """Store the data of channel on data storage
    
    Arguments:
        channel (list): List of channel

    Returns:
        True if the channel data stored successfully
        False if fail to store channel data
    """
    data = get_data()

    data["channels"].append(channel)

    with open(data_path, 'w') as f:
        json.dump(data, f)

    if get_channels() == data["channels"]:
        return True
    return False

def append_channel_all_members(channel_id: int, u_id: int) -> None:
    """TODO"""
    data = get_data()

    data["channels"][channel_id-1]['all_members'].append(u_id)

    with open(data_path, 'w') as f:
        json.dump(data, f)
