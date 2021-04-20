"""Helpers for mainly but not limited to the base funcitons"""

from src.data.helper import get_users, get_channels, get_data,update_owner_members, update_all_members, get_message_count, \
                            get_dms, update_user_all_channel_message, update_user_all_dm_message, update_message, \
                            update_dm_users, store_reset_code, remove_reset_code
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
                'permission_id' : user['permission_id'],
                'profile_img_url': user['profile_img_url']
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
                'is_public' : channel['is_public'],
                'standup': channel['standup'],
            }
    return {}

'''
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
'''
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

def user_is_channel_member(channel_id: int, auth_user_id: int) -> bool:
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

def user_is_channel_owner(channel_id: int, auth_user_id: int) -> bool:
    """A function when passed a channel and authenticated user ID, checks if they are the owner

    Arguments: 
        channel_id : ID of channel
        auth_user_id: ID of an authenticated user

    Return Values:
        True: if the user is an owner of the channel
        False: if the user is not an owner of the channel
    """        
    channel = get_channel(channel_id)
    owners = channel.get('owner_members')
    if not owners:
        # don't iterate over NoneType
        return False
    for owner in owners:
        if owner.get('u_id') == auth_user_id:
            return True
    return False

def user_is_dm_owner(dm_id: int, auth_user_id: int) -> bool:
    """A function that checks if a user is the owner of a dm

    Arguments: 
        channel_id : ID of channel
        auth_user_id: ID of an authenticated user

    Return Values:
        True: if the user is an owner of the channel
        False: if the user is not an owner of the channel
    """        
    dm = get_dm(dm_id)
    dm_owner = dm.get('auth_user_id')
    return dm_owner == auth_user_id

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

def get_user_from_handlestr(handlestr: str) -> dict:
    """Get user data of user with handlestr provided

    Arguements:
        handlestr (str): handlestr of user

    Returns:
        Returns user data
    """   
    users = get_current_users()
    for user in users:
        if handlestr == user.get('handle_str'):
            return user
    return None

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
    dm = get_dm(dm_id)
    if u_id in dm['u_ids']:
        return True
    return False

def new_message_id() -> int:
    #To correctly use, must create message then store the message. If you do not
    #Store the message this count WILL NOT change
    #E.g, when first started, this will return int 1, then when called again
    #After message is stored this will return 2 etc etc
    return get_message_count() + 1

def create_message(auth_user_id: int, message: str, channel_id=None, dm_id=None) -> dict:
    timenow = datetime.utcnow()
    timestamp = int(timenow.replace(tzinfo=timezone.utc).timestamp())

    if channel_id:
        msg = {
            'message_id' : new_message_id(),
            'channel_id' : channel_id,
            'u_id' : auth_user_id,
            'message' : message,
            'time_created' : timestamp,
            'reacts' : [{'react_id' : 1,
                        'u_ids' : [],
                        'is_this_user_reacted' : False
                    }],
            'is_pinned' : False
        }
    else:
        msg = {
            'message_id' : new_message_id(),
            'dm_id' : dm_id,
            'u_id' : auth_user_id,
            'message' : message,
            'time_created' : timestamp,
            'reacts' : [{'react_id' : 1,
                        'u_ids' : [],
                        'is_this_user_reacted' : False
                    }],
            'is_pinned' : False
        }
    return msg

def remove_from_owner_members(channel_id : int, auth_user_id: int) -> None:
    
    owner_member = get_channel(channel_id)['owner_members']
    user = get_user(auth_user_id)
    owner_member.remove(user)
    update_owner_members(channel_id, owner_member)

def remove_from_all_members(channel_id : int, auth_user_id: int) -> None:
    
    all_member = get_channel(channel_id)['all_members']
    user = get_user(auth_user_id)
    all_member.remove(user)
    update_all_members(channel_id, all_member)

def remove_from_dm_members(dm_id : int, u_id: int) -> None:
    
    dm_members = get_dm(dm_id).get('u_ids')
    dm_members.remove(u_id)
    update_dm_users(dm_members, dm_id)     

def create_dm_name(u_ids: list) -> str:
    
    # iterate over all users and populate with respected handle_str
    handle_strs = [get_user(u_id).get('handle_str') for u_id in u_ids]

    # sort to obtain correct order as per spec
    handle_strs.sort()
    output = ', '.join(handle_strs)
    
    return output

def remove_user(u_id: int) -> None:
    channels = get_channels()
    for channel in channels:
        if user_is_channel_owner(channel.get('channel_id'), u_id):
            remove_from_owner_members(channel['channel_id'], u_id) # remove user from owner_member
        if user_is_channel_member(channel.get('channel_id'), u_id):
            remove_from_all_members(channel['channel_id'], u_id)  # remove user from all member
            update_user_all_channel_message(u_id, channel['channel_id'], 'Removed user')

    dms = get_dms()
    for dm in dms:
        if user_is_dm_member(dm['dm_id'], u_id):
            remove_from_dm_members(dm['dm_id'], u_id)
            update_user_all_dm_message(u_id, dm['dm_id'], 'Removed user')


def get_message_ch_id_or_dm_id(message_id: int) -> dict:
    """Get a channel_id or dm_id from a message_id
    returns a dict with only key channel_id, dm_id or None"""
    channels = get_channels()
    for channel in channels:
        # look for message in channels
        for message in channel.get('messages'):
            if message.get('message_id') == message_id:
                return {'channel_id': channel.get('channel_id')}

    """Get a dm_id from a message_id"""
    dms = get_dms()
    for dm in dms:
        # look for message in dms
        for message in dm.get('messages'):
            if message.get('message_id') == message_id:
                return {'dm_id': dm.get('dm_id')}
    return {}


def remove_message(message_id: int, channel_id=None, dm_id=None) -> bool:
    """Remove a message from a channel or dm"""
    if channel_id:
        update_message(message_id, channel_id=channel_id)
        return True
    else:
        update_message(message_id, dm_id=dm_id)
        return True

def edit_message(message_id: int, message: str, channel_id=None, dm_id=None) -> bool:
    """Remove a message from a channel"""
    if channel_id:
        update_message(message_id, message=message, channel_id=channel_id)
        return True
    else:
        update_message(message_id, message=message, dm_id=dm_id)
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

def get_user_by_email(email: str) -> dict:
    """ Get user(dictionary) from email
    Only for current users.

    Arguments:
        email (str) - Email for a user.
 
    Return Value:
        Returns user(dictionary) on a user with the same email.
        Returns empty(dictionary) on no user with the email.

    """
    for user in get_current_users():
        if user['email'] == email:
            return user
    return {}        

def get_user_by_reset_code(reset_code: str) -> dict: # pragma: no cover
    # this function is used exclusivley in http routes
    for user in get_current_users():
        if user['reset_code'] == reset_code:
            return user
    return {} 

def format_share_message(og_message: str, optional_message: str) -> str:
    output = f'{optional_message}\n\n"""\n{og_message}\n"""'
    return output

def get_message(message_id: int) -> str:
    channels = get_channels()
    for channel in channels:
        # look for message in channels
        for message in channel.get('messages'):
            if message.get('message_id') == message_id:
                return message.get('message')

    dms = get_dms()
    for dm in dms:
        # look for message in dms
        for message in dm.get('messages'):
            if message.get('message_id') == message_id:
                return message.get('message')
    return {}


def get_notifications(u_id: int) -> list:
    users = get_users()
    for user in users:
        if user.get('u_id') == u_id:
            return user.get('notifications')
    return None

def get_channel_name(channel_id: int) -> str:
    for channel in get_channels():
        if channel.get('channel_id') == channel_id:
            return channel.get('name')
    return None

def get_dm_name(dm_id: int) -> str:
    for dm in get_dms():
        if dm.get('channel_id') == dm_id:
            return dm.get('name')
    return None

def create_notification(channel_id: int, dm_id: int, u_id: int, added = False, tagged = False, msgs = '') -> dict:
    user = get_user(u_id)

    handle_str = user.get('handle_str')

    if added:
        if channel_id != -1:
            name = get_channel_name(channel_id)
            notification_message = f"{handle_str} added you to {name}"
            notification = {
                'channel_id': channel_id,
                'dm_id': dm_id,
                'notification_message': notification_message
            }

        if dm_id != -1:
            name = get_dm_name(dm_id)
            notification_message = f"{handle_str} added you to {name}"
            notification = {
                'channel_id': channel_id,
                'dm_id': dm_id,
                'notification_message': notification_message
            }
    if tagged:
        if channel_id != -1:
            name = get_channel_name(channel_id)
            msg = msgs[0:20]
            notification_message = f"{handle_str} tagged you in {name}: {msg}"
            notification = {
                'channel_id': channel_id,
                'dm_id': dm_id,
                'notification_message': notification_message
            }
        if dm_id != -1:
            name = get_dm_name(dm_id)
            msg = msgs[0:20]
            notification_message = f"{handle_str} tagged you in {name}: {msg}"
            notification = {
                'channel_id': channel_id,
                'dm_id': dm_id,
                'notification_message': notification_message
            }

    return notification

def tagged_handlestrs(message: str):
    """A function that when passed an message, will return a list of handlestr that being tagged

    Arguments:
        message (str): message being sent to a channel or dm

    Return Values:
        handle_strs(dict): A dictionary of handlestrs that being tagged 
    """    
    msg = message
    start = 0
    handle_strs = []
    while msg.find('@') != -1:
        start = msg.find('@')

        msg = msg[start + 1:]
        
        end = msg.find(' ')
        if end == -1:
            end =  len(msg)

        handle_str = msg[0:end]
        handle_strs.append(handle_str)
        if handle_str.find('@') != -1:
            continue

        msg = msg[end:]
    return {'handle_strs': handle_strs}

def is_pinned(message_id: int) -> bool:
    channels = get_channels()
    for channel in channels:
        # look for message in channels
        for message in channel.get('messages'):
            if message.get('message_id') == message_id:
                if message.get('is_pinned') == True:
                    return True

    dms = get_dms()
    for dm in dms:
        # look for message in dms
        for message in dm.get('messages'):
            if message.get('message_id') == message_id:
                if message.get('is_pinned') == True:
                    return True

    return False

def get_react_uids(message_id: int) -> list:
    channels = get_channels()
    for channel in channels:
        # look for message in channels
        for message in channel.get('messages'):
            if message.get('message_id') == message_id:
                react_list = message.get('reacts')
                return react_list[0].get('u_ids')

    dms = get_dms()
    for dm in dms:
        # look for message in dms
        for message in dm.get('messages'):
            if message.get('message_id') == message_id:
                react_list = message.get('reacts')
                return react_list[0].get('u_ids')

def check_valid_message(message_id: int) -> str:
    channels = get_channels()
    for channel in channels:
        # look for message in channels
        for message in channel.get('messages'):
            if message.get('message_id') == message_id:
                return True

    dms = get_dms()
    for dm in dms:
        # look for message in dms
        for message in dm.get('messages'):
            if message.get('message_id') == message_id:
                return True
    return False

def create_user_stats() -> dict:
    stats = {
        'channels_joined' : [{
                            'num_channels_joined' : 0,
                            'time_stamp' : []
                            }],
        'dms_joined' : [{
                        'num_dms_joined' : 0,
                        'time_stamp' : []
                        }],
        'messages_sent' : [{
                            'num_messages_sent' : 0,
                            'time_stamp' : []
                            }],
        'involvement_rate' : 0
    }

    return stats

def edit_reset_code(email: str, reset_code = None) -> None: # pragma: no cover
    # this function is used exclusivley in http routes
    """Reset/remove or store an email address based on optional parameter reset_code"""
    user = get_user_by_email(email)
    u_id = user.get('u_id')

    if not reset_code:
        remove_reset_code(u_id)
    else:
        store_reset_code(u_id, reset_code)
