from src.config import data_path
import json

def clear_data() -> None:
    """ Resets the internal data of the application to it's initial state
    
    Return Value:
        Return Value None on clearing of data
    """

    cleared_data = {
        'users': [],
        'channels': []
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

def get_user_index(u_id: int) -> int:
    """TODO"""
    data = get_data()
    for idx in range(len(data)-1):
        if data['users'][idx]['u_id'] == u_id:
            return idx
    return -1

def get_channel_index(channel_id: int) -> int:
    """TODO"""
    data = get_data()
    for idx in range(len(data)-1):
        if data['channels'][idx]['channel_id'] == channel_id:
            return idx
    return -1

def get_users() -> list:
    """Get list of user from data storage
    
    Arguments:
        This function takes no argument

    Return Value:
        users (list): List of users
    """
    return get_data().get('users')

def get_channels() -> list:
    """Get list of channel from data storage
    
    Arguments:
        This function takes no argument

    Return Value:
        channels (list): List of channels
    """
    return get_data().get('channels')


def store_user(user: dict) -> None:
    """store the data of user on data storage
    
    Arguments:
        user (dict): a user

    Return Value:
        Returns None
    """
    data = get_data()
    data.get('users').append(user)

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_name_first(u_id: int, name_first: str) -> None:
    """Update the user's first name
    
    Arguments:
        u_id (int) - The user's id
        name_first (str) - The user's last name

    Return Value:
        Returns None if updated user's first name successfully
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['name_first'] = name_first

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
    idx = get_user_index(u_id)

    data['users'][idx]['name_last'] = name_last

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
    idx = get_user_index(u_id)

    data['users'][idx]['email'] = email

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
    idx = get_user_index(u_id)

    data['users'][idx]['handle_str'] = handle_str 

    with open(data_path, 'w') as f:
        json.dump(data, f)

def store_channel(channel: dict) -> bool:
    """Store the data of channel on data storage

    Arguments:
        channel (list): List of channel

    Return Value:
        True if the channel data stored successfully
        False if fail to store channel data
    """
    data = get_data()

    data['channels'].append(channel)

    with open(data_path, 'w') as f:
        json.dump(data, f)

    if get_channels() == data["channels"]:
        return True
    return False

def append_channel_all_members(channel_id: int, user: dict) -> None:
    """TODO"""
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['all_members'].append(user)

    with open(data_path, 'w') as f:
        json.dump(data, f)

def append_channel_owner_members(channel_id: int, user: dict) -> None:
    """TODO"""
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['owner_members'].append(user)

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_owner_members(channel_id : int, owner_members: list) -> None:
    """TODO"""
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['owner_members'] = owner_members 

    with open(data_path, 'w') as f:
        json.dump(data, f)

def update_all_members(channel_id : int, all_members: list) -> None:
    """TODO"""
    data = get_data()
    # TODO: bad to index here (channel_id-1) should loop ofer users data
    idx = get_channel_index(channel_id)

    data['channels'][idx]['all_members'] = all_members 

    with open(data_path, 'w') as f:
        json.dump(data, f)