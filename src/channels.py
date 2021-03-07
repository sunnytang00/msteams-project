from .data import data
from .error import InputError, AccessError
from .helper import user_exists, get_user_data, get_channel_data, user_is_member, valid_channel_name

"""
Create and show the list of channels

This module demonstrates creation of channels and ability of showing list of channels with associated details
as specified by the COMP1531 Major Project specification.
"""

def channels_list_v1(auth_user_id):
    """ Shows the list of channels and the associated details that authorised user is part of

    Arguments: 
        auth_user_id (int) - ID of authorised user

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 

    Return Value:
        channels_of_user (list) - a list contains channels that the user is part of 
    """
    
    if not user_exists(auth_user_id):
        raise AccessError('User ID is invaild')

    if len(data['channels']) == 0:
        return {}

    channels_of_user = {
                    'channels': [

                    ]
                }

    for channel in data['channels']:
        if user_is_member(channel, auth_user_id):
            channels_of_user['channels'].append(channel)
    
    return channels_of_user

def channels_listall_v1(auth_user_id):
    """ Shows all the channels on the list and their details
    
    Arguments: 
        auth_user_id (int) - ID of authorised user

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 

    Return Value:
        data['channels'] (list) - A list contains all the public channels stored in the storage
    """
    if not user_exists(auth_user_id):
        raise AccessError('User ID is invaild')

    public_channels = []
    for channel in data['channels']:
        if user_is_member(channel, auth_user_id) or channel['is_public']:
            public_channels.append(channel)
    return public_channels

def channels_create_v1(auth_user_id, name, is_public):
    """ Create a public/private channel with specified name and owned by user with specified ID
        
    Arguments: 
        auth_user_id (int) - ID of authorised user
        name (str) - Name for the new channel
        is_public (bool) - Flags that indicate the channel is public or private

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 
        InputError - Occurs when the length of name is too long
        InputError - Occurs when the channel with specified name already exists

    Return Value:
        ｛'channel_id'｝ (dict) - A dictonary that contains the ID of channel created
    """
    global data

    if not user_exists(auth_user_id):
        raise AccessError('User ID is invaild')

    if valid_channel_name(name):
        raise InputError(f'Name {name} is more than 20 characters long')

    user = get_user_data(auth_user_id) 

    channel_id = len(data['channels']) + 1

    email = user['email']
    name_first = user['name_first']
    name_last = user['name_last']
    handle_str = user['handle_str']

    data['channels'].append({
        'channel_id': channel_id,
        'name': name,
        'owner_members': [
            {
                'u_id': auth_user_id,
                'email': email,
                'name_first': name_first,
                'name_last': name_last,
                'handle_str': handle_str,
            }
        ],
        'all_members': [
            {
                'u_id': auth_user_id,
                'email': email,
                'name_first': name_first,
                'name_last': name_last,
                'handle_str': handle_str,
            }
        ],
        'messages': [],
        'is_public': is_public
    })

    return {
        'channel_id': channel_id,
    }
