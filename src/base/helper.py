"""TODO"""

from src.data.helper import get_users, get_channels, get_data,update_owner_members, update_all_members, get_message_count, \
                            get_dms, update_user_all_channel_message, update_user_all_dm_message, update_message, \
                            update_dm_users
from src.routes.helper import decode_token
import re
from datetime import timezone, datetime
import time
from collections import namedtuple

def valid_email(email: str) -> bool:
    """Check if email is valid

    Arguments:
        email (str) - The users email address.

    Return Values:
        Returns bool on regexp evalutaion
    """

    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    return re.search(regex, email)

def get_current_users() -> list:
    """ function that returned list of user that was not removed 

    Returns:
        current_user (list): user in user list that was not removed
    """

    current_user = []
    users = get_users()
    for user in users:
        if not user['removed']:
            current_user.append(user)
    return current_user

def get_current_user(auth_user_id: int) -> list:
    """A function that when passed an authenticated user id, will return their user id, email, password, first name and last name
       if the user is not removed from the Dream

    Arguments:
        auth_user_id (int): ID of authorised user

    Return Values:
        dict: A dictionary of their email, password, first name and last name
        empty dict if user isn't found
    """    
    for user in get_current_users():
        if user['u_id'] == auth_user_id:
            return {
                'u_id' : auth_user_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id' : user['permission_id']
            }
    return {}


def get_user(auth_user_id: int) -> dict:
    """A function that when passed an authenticated user id, will return their user id, email, password, first name and last name

    Arguments:
        auth_user_id (int): ID of authorised user

    Return Values:
        dict: A dictionary of their email, password, first name and last name
        empty dict if user isn't found
    """    
    for user in get_users():
        if user['u_id'] == auth_user_id:
            return {
                'u_id' : auth_user_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id' : user['permission_id']
            }
    return {}

def get_channel(channel_id: int) -> dict:
    """Function that when passed a channel id, will get the id, name, auth_user_id, owners, all members, messages and whether it is public

    Arguments:
        channel_id (int): ID of the channel

    Return Values:
        dict: A dict of the id, name, auth_user_id, owners, all members, messages and whether it is public of the channel if it is found
        empty dict if the id does not match a channel
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
    return {}

def get_dm_data(dm_id : int) -> dict:
    """Function that when a passed a dm id, will get the id, dm_name and u_ids that refers to member of dm

    Arguments:
        dm_id (int) : ID of the dm
    
    Returns Values:
        dm_data (dict) : dictionary that contains dm_id, dm_name and u_ids, empty if dm with dm_id is not found
    """

    for dm in get_dms():
        if dm['dm_id'] == dm_id:
            return {
                'dm_id': dm['dm_id'],
                'dm_name': dm['dm_name'],
                'u_ids': dm['u_ids']
            }
    return {}

def get_dm(dm_id: int) -> dict:
    """Function that when a passed a dm id, will get the id, dm_name and u_ids that refers to member of dm

    Arguments:
        dm_id (int) : ID of the dm
    
    Returns Values:
        dm_data (dict) : dictionary that contains dm_id, dm_name and u_ids, empty if dm with dm_id is not found
    """

    for dm in get_dms():
        if dm['dm_id'] == dm_id:
            return {
                'auth_user_id': dm['auth_user_id'],
                'dm_id': dm['dm_id'],
                'dm_name': dm['dm_name'],
                'u_ids': dm['u_ids'],
                'messages': dm['messages']
            }
    return {}

def user_is_member(channel_id: int, auth_user_id: int) -> bool:
    """A function that when passed a channel and an ID of an authenticated user, will check if it is a member of the channel

    Arguments:
        channel_id : ID of channel
        auth_user_id (int): ID of authenticated user

    Return Values:
        True: if the ID of the user is a member of the channel
        False: if the user is not a member of the channel
    """    
    channel = get_channel(channel_id)
    for user in channel['all_members']:
        if auth_user_id == user['u_id']:
            return True
    return False

def user_is_owner(channel_id: int, auth_user_id: int) -> bool:
    """A function when passed a channel and authenticated user ID, checks if they are the owner

    Arguments: 
        channel_id : ID of channel
        auth_user_id: ID of an authenticated user

    Return Values:
        True: if the user is an owner of the channel
        False: if the user is not an owner of the channel
    """        
    channel = get_channel(channel_id)
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
    """Check if there is user with u_id is owner of Dream
    
    Arguments:
        u_id (int): id of user

    Returns:
        True: if user with u_id is owner of Dream
        False: if user with u_id is not owner of Dream
    """
    for user in get_users():
        if u_id == user['u_id']:
            if user['permission_id'] == 1:
                return True
    return False

def user_is_dm_member(dm_id: int, u_id: int) -> bool:
    """ Check if there is user with u_id is member of dm

    Arguments:
        dm_id (int) : id of dm
        u_id (int)  : id of user
    
    Returns:
        True: if user with u_id is member of dm
        False: if user with u_id is not member of dm
    """
    dm = get_dm_data(dm_id)
    if u_id in dm['u_ids']:
        return True
    return False

def new_message_id(channel_id: int) -> int:
    #To correctly use, must create message then store the message. If you do not
    #Store the message this count WILL NOT change
    #E.g, when first started, this will return int 1, then when called again
    #After message is stored this will return 2 etc etc
    return get_message_count() + 1

def create_message(auth_user_id: int, channel_id: int, message: str) -> dict:
    timenow = datetime.utcnow()
    timestamp = int(timenow.replace(tzinfo=timezone.utc).timestamp())

    return {
        'message_id' : new_message_id(channel_id),
        'channel_id' : channel_id,
        'u_id' : auth_user_id,
        'message' : message,
        'time_created' : timestamp
    }


def remove_from_owner_members(channel_id : int, auth_user_id: int) -> None:
    """TODO"""
    owner_member = get_channel(channel_id)['owner_members']
    user = get_user(auth_user_id)
    owner_member.remove(user)
    update_owner_members(channel_id, owner_member)

def remove_from_all_members(channel_id : int, auth_user_id: int) -> None:
    """TODO"""
    all_member = get_channel(channel_id)['all_members']
    user = get_user(auth_user_id)
    all_member.remove(user)
    update_all_members(channel_id, all_member)

def remove_from_dm_members(dm_id : int, u_id: int) -> None:
    """TODO"""
    dm_members = get_dm(dm_id).get('u_ids')
    dm_members.remove(u_id)
    update_dm_users(dm_members, dm_id)     

def get_dm_name(u_ids: list) -> str:
    """TODO"""
    # iterate over all users and populate with respected handle_str
    handle_strs = [get_user(u_id).get('handle_str') for u_id in u_ids]

    # sort to obtain correct order as per spec
    handle_strs.sort()
    output = ', '.join(handle_strs)
    
    return output

def remove_user(u_id: int) -> None:
    """
    TODO:   when a user being removed, all member list should remove the user out 
            and functions that return users stuff should not have those users
    should keep this function update if there is new type of list of user 

    member list that needs to change:
        channels:
            owner_member
            all_member
        
    """
    channels = get_channels()
    for channel in channels:
        if user_is_owner(channel.get('channel_id'), u_id):
            remove_from_owner_members(channel['channel_id'], u_id) # remove user from owner_member
        if user_is_member(channel.get('channel_id'), u_id):
            remove_from_all_members(channel['channel_id'], u_id)  # remove user from all member
            update_user_all_channel_message(u_id, channel['channel_id'], 'Removed user')

    dms = get_dms()
    for dm in dms:
        if user_is_dm_member(dm['dm_id'], u_id):
            remove_from_dm_members(dm['dm_id'], u_id)
            update_user_all_dm_message(u_id, dm['dm_id'], 'Removed user')


def get_message_channel_id(message_id: int) -> int:
    """TODO
    """
    channels = get_channels()
    for channel in channels:
        for message in channel.get('messages'):
            if message.get('message_id') == message_id:
                return channel.get('channel_id')
    return None

def remove_message(message_id: int) -> bool:
    """TODO"""
    channel_id = get_message_channel_id(message_id)
    if not channel_id:
        return False
    else:
        update_message(message_id, channel_id, remove=True)
        return True

def token_to_auth_user_id(token: str) -> int:
    """Get auth_user_id from a token
    can also be used to see if token is valid
    """
    session_id = decode_token(token)
    for user in get_users():
        for session in user.get('session_list'):
            if session == session_id:
                return user.get('u_id')
    return None
