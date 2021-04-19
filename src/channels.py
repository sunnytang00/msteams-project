""" Create and show the list of channels

This module demonstrates creation of channels and ability of showing list of channels with associated details
as specified by the COMP1531 Major Project specification.
"""

from src.error import InputError, AccessError
from src.helper import get_user, get_channel, user_is_channel_member, valid_channel_name, get_current_user
from src.data.helper import get_channels, store_channel, get_channel_count, update_user_stats_channels

def channels_list_v1(auth_user_id):
    """ Shows the list of channels and the associated details that authorised user is part of

    Arguments: 
        auth_user_id (int) - ID of authorised user

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 

    Return Value:
        Returns channels_of_user (list) on valid authenticated user
    """
    
    if not get_current_user(auth_user_id):
        raise AccessError(f'User ID {auth_user_id} is invaild')

    if len(get_channels()) == 0:
        return {'channels' : []}

    channels_of_user = {
                    'channels': [

                    ]
                }

    for channel in get_channels():
        if user_is_channel_member(channel.get('channel_id'), auth_user_id):
            channels = {}
            channels['channel_id'] = channel['channel_id']
            channels['name'] = channel['name']
            channels_of_user['channels'].append(channels)
    
    return channels_of_user

def channels_listall_v1(auth_user_id):
    """ Shows all the channels on the list and their details
    
    Arguments: 
        auth_user_id (int) - ID of authorised user

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 

    Return Value:
        Returns get_channels() (list) on valid authenticated user
    """
    if not get_current_user(auth_user_id):
        raise AccessError(f'User ID {auth_user_id} is invaild')

    public_channels = {'channels': []}
    for channel in get_channels():
        if user_is_channel_member(channel['channel_id'], auth_user_id) or channel['is_public']:
            channels = {}
            channels['channel_id'] = channel['channel_id']
            channels['name'] = channel['name']
            public_channels['channels'].append(channels)
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

    Return Value:
        Returns ｛'channel_id'｝ (dict) on valid authenticated user and valid name
    """

    if not get_current_user(auth_user_id):
        raise AccessError(f'User ID {auth_user_id} is invaild')

    if valid_channel_name(name):
        raise InputError(f'Name {name} is more than 20 characters long')

    channel_id = get_channel_count() + 1

    user = get_user(auth_user_id)

    channel = {
        'channel_id': channel_id,
        'name': name,
        'owner_members': [user],
        'all_members': [user],
        'messages': [],
        'is_public': is_public,
        'standup': {'active': False, 'time_finish': None, 'buffer': []}
    }
    store_channel(channel)
    update_user_stats_channels(auth_user_id, 'add')

    return {
        'channel_id': channel_id,
    }
