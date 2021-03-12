""" Create and show the list of channels

This module demonstrates creation of channels and ability of showing list of channels with associated details
as specified by the COMP1531 Major Project specification.
"""

from src.data.data import data
from src.base.error import InputError, AccessError
from src.base.helper import user_exists, get_user_data, get_channel_data, user_is_member, valid_channel_name

def channels_list_v1(auth_user_id):
    """ Shows the list of channels and the associated details that authorised user is part of

    Arguments: 
        auth_user_id (int) - ID of authorised user

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 

    Return Value:
        Returns channels_of_user (list) on valid authenticated user
    """
    
    if not user_exists(auth_user_id):
        raise AccessError(f'User ID {auth_user_id} is invaild')

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
        Returns data['channels'] (list) on valid authenticated user
    """
    if not user_exists(auth_user_id):
        raise AccessError(f'User ID {auth_user_id} is invaild')

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
        Returns ｛'channel_id'｝ (dict) on valid authenticated user and valid name
    """
    global data

    if not user_exists(auth_user_id):
        raise AccessError(f'User ID {auth_user_id} is invaild')

    if valid_channel_name(name):
        raise InputError(f'Name {name} is more than 20 characters long')

    channel_id = len(data['channels']) + 1

    data['channels'].append({
        'channel_id': channel_id,
        'name': name,
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'messages': [],
        'is_public': is_public
    })

    return {
        'channel_id': channel_id,
    }
