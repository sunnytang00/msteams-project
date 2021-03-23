"""TODO"""

from src.data.helper import get_users, get_channels, get_data,update_owner_members, update_all_members
import re

def valid_email(email: str) -> bool:
    """Check if email is valid

    Arguments:
        email (str) - The users email address.

    Return Values:
        Returns bool on regexp evalutaion
    """

    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    return re.search(regex, email)

def user_exists(auth_user_id: int) -> bool:
    """Function that when passed auth_user_id, will check if the user already exists

    Arguments:
        auth_user_id (int): ID of authorised user

    Return Values:
       True: if user exists
       False: if user does not exist
    """    
    for user in get_users():
        if user['u_id'] == auth_user_id:
            return True
    return False

def channel_exists(channel_id: int) -> bool:
    """Function that when passed channel id, check if it exists

    Arguments:
        channel_id (int): The unique id of the channel

    Return Values:
        True: if channel exists
        False: if channel does not exist
    """    
    for channel in get_channels():
        if channel['channel_id'] == channel_id:
            return True
    return False

def get_user_data(auth_user_id: int) -> dict:
    """A function that when passed an authenticated user id, will return their user id, email, password, first name and last name

    Arguments:
        auth_user_id (int): ID of authorised user

    Return Values:
        dict: A dictionary of their email, password, first name and last name
        None: if nothing is found
    """    
    for user in get_users():
        if user['u_id'] == auth_user_id:
            return {
                'u_id' : auth_user_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }
    return None

def get_channel_data(channel_id: int) -> dict:
    """Function that when passed a channel id, will get the id, name, user_id, owners, all members, messages and whether it is public

    Arguments:
        channel_id (int): ID of the channel

    Return Values:
        dict: A dict of the id, name, user_id, owners, all members, messages and whether it is public of the channel if it is found
        None: if the id does not match a channel
    """    
    for channel in get_channels():
        if channel['channel_id'] == channel_id:
            return {
                'channel_id': channel['channel_id'],
                'name': channel['name'],
                'owner_members': channel['owner_members'],
                'all_members' : channel['all_members'],
                'messages' : channel['messages'],
                'is_public' : channel['is_public']
            }
    return None

def user_is_member(channel: dict, auth_user_id: int) -> bool:
    """A function that when passed a channel and an ID of an authenticated user, will check if it is a member of the channel

    Arguments:
        channel (dict): A dictionary of the channel data
        auth_user_id (int): ID of authenticated user

    Return Values:
        True: if the ID of the user is a member of the channel
        False: if the user is not a member of the channel
    """    
    for user in channel['all_members']:
        if auth_user_id == user['u_id']:
            return True
    return False

def user_is_owner(channel: dict, auth_user_id: int) -> bool:
    """A function when passed a channel and authenticated user ID, checks if they are the owner

    Arguments: 
        channel (dict): A dictionary of the channel data
        auth_user_id: ID of an authenticated user

    Return Values:
        True: if the user is an owner of the channel
        False: if the user is not an owner of the channel
    """        
    for owner in channel['owner_members']:
        if owner['u_id'] == auth_user_id:
            return True
    return False

def valid_password(password: str) -> bool:
    """A function that when passed password, will check if the length is greater than 6

    Arguments:
        password (str): A string of characters to be the password

    Return Values:
        True: if the password length is greater than 6
        False: if the password is shorter than 6 characters
    """    
    return len(password) >= 6

def valid_first_name(name_first: str) -> bool:
    """A function that when passed the first name, will check whether it is between and including 1 and 50 characters

    Arguements:
        name_first (str): The first name of the user

    Returns:
        True: if it is a valid first name
        False: if the first name is longer than 50 characters or shorter than 1 character
    """    
    return len(name_first) in range(1, 51)

def valid_last_name(name_last: str) -> bool:
    """A function that when passed the last name, will check whether it is between and including 1 and 50 characters

    Arguements:
        name_last (str): Last name of the user

    Returns:
        True: if the last name is valid
        False: if the last name is longer than 50 characters or shorter than 1 character
    """    
    # check last name length is in [1, 50]
    return len(name_last) in range(1, 51)

def email_exists(email: str) -> bool:
    """A function that when passed an email, will check if it already exists

    Arguements:
        email (str): Email of the user

    Returns:
        True: if the email exists
        False: if the email does not already exist
    """    
    # check if email already exists in data
    for user in get_users():
        if user.get('email') == email:
            return True
    return False

def valid_channel_name(name: str) -> bool:
    """A function that when passed name, will check whether the channel name is over 20 characters

    Arguements:
        name (str): Name of channel

    Returns:
        True: if the name is valid
        False: if the name is under 20 characters
    """    
    return len(name) > 20

def handle_str_exists(handle_str: str) -> bool:
    """A function that when passed name, will check whether the handle string name is over 20 characters

    Arguements:
        name (str): Handle string
    Returns:
        True: if exists
        False: if not exists
    """   
    for user in get_users():
        if user.get('handle_str') == handle_str:
            return True
    return False

def get_handle_str(name_first: str, name_last: str) -> str:
    """Generates a handle_str

    Arguements:
        name_first (str): First name of user
        name_last (str): Last name of user

    Returns:
        Returns handle_str
    """   
    handle_str = (name_first + name_last).replace(' ', '').replace('@', '').lower()[:20]
    count = 0
    while handle_str_exists(handle_str):
        handle_str = (name_first + name_last).replace(' ', '').replace('@', '').lower()[:20]
        handle_str += str(count)
        count += 1

    return handle_str

def same_name_user_exist(name_first: str, name_last: str) -> str:
    """Check if there is user with same name already exists on the database
    
    Arguments:
        name_first (str): First name of user
        name_last (str): Last name of user

    Returns:
        True: if exists
        False: if not exists
    """
    for user in get_users():
        if name_first == user['name_first'] and name_last == user['name_last']:
            return True
    return False

def user_is_Dream_owner(u_id: int) -> bool:
    #TODO owner of Dream should checked by permission id, may need to change stucture of user data?
    #by default the very first user that registered is user of Dream
    """Check if there is user with u_id is owner of Dream
    
    Arguments:
        u_id (int): id of user

    Returns:
        True: if user with u_id is owner of Dream
        False: if user with u_id is not owner of Dream
    """
    users = get_users()
    if u_id == users[0]['u_id']:
        return True
    else:
        return False

def remove_from_owner_members(channel_id : int, user_id: int) -> None:
    """TODO"""
    owner_member = get_channel_data(channel_id)['owner_members']
    user = get_user_data(user_id)
    owner_member.remove(user)
    update_owner_members(channel_id, owner_member)

def remove_from_all_members(channel_id : int, user_id: int) -> None:
    """TODO"""
    all_member = get_channel_data(channel_id)['all_members']
    user = get_user_data(user_id)
    all_member.remove(user)
    update_all_members(channel_id, all_member)
        