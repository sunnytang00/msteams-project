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
    """ Resets the internal data of the application to it's initial state
    
    Return Value:
        Return Value None on clearing of data
    """

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

    Return Value:
        data (dict): data stored on the data storage
    """
    with open(data_path, 'r') as f:
        data = json.load(f)

    return data


def get_users() -> list:
    """Get list of user from data storage
    
    Arguments:
        This function takes no argument

    Return Value:
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

    Return Value:
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

def update_name_first(u_id: int, name_first: str) -> None:
    """Update the user's first name
    
    Arguments:
        u_id (int) - The user's id
        name_first (str) - The user's last name

    Return Value:
        Returns None if updated user's first name successfully
    """

    data = get_data()

    data["users"][u_id-1]["name_first"] = name_first

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_name_last(u_id: int, name_last: str) -> None:
    """Update the user's last name
    
    Arguments:
        u_id (int) - The user's id
        name_last (str) - The user's last name

    Return Value:
        Returns None if updated user's last name successfully
    """

    data = get_data()

    data["users"][u_id-1]["name_last"] = name_last

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_email(u_id: int, email: str) -> None:
    """Update the user's email
    
    Arguments:
        u_id (int) - The user's id
        email (str) - The user's handle

    Return Value:
        Returns None if updated user's email successfully
    """

    data = get_data()

    data["users"][u_id-1]["email"] = email

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_handle_str(u_id: int, handle_str: str) -> None:
    """Update the user's handle (i.e. display name)
    
    Arguments:
        u_id (int) - The user's id
        handle_str (str) - The user's handle

    Return Value:
        Returns None if updated user's handle_str successfully
    """
    data = get_data()

    data["users"][u_id-1]["handle_str"] = handle_str 

    with open(data_path, 'w') as f:
        json.dump(data, f)

def store_channel(channel: list) -> bool:
    """Store the data of channel on data storage
    
    Arguments:
        channel (list): List of channel

    Return Value:
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

def append_channel_all_members(channel_id: int, user: dict) -> None:
    """TODO"""
    data = get_data()

    data["channels"][channel_id-1]['all_members'].append(user)

    with open(data_path, 'w') as f:
        json.dump(data, f)

def append_channel_owner_members(channel_id: int, user: dict) -> None:
    """TODO"""
    data = get_data()
    
    data["channels"][channel_id-1]['owner_members'].append(user)

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_owner_members(channel_id : int, owner_members: list) -> Nonek:
    """TODO"""
    data = get_data()

    data["channels"][channel_id-1]["owner_members"] = owner_members 

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_all_members(channel_id : int, all_members: list) -> None:
    """TODO"""
    data = get_data()

    data["channels"][channel_id-1]["all_members"] = all_members 

    with open(data_path, 'w') as f:
        json.dump(data, f)