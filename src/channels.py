from src.data import data
from src.error import InputError, AccessError
"""
Create and show the list of channels

This module demonstrates creation of channels and ability of showing list of channels with associated details
as specified by the COMP1531 Major Project specification.
"""

def channels_list_v1(auth_user_id):
    """ 
    Shows the list of channels and the associated details that authorised user is part of

    Arguments: 
        auth_user_id (int) - ID of authorised user

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 

    Return Value:
        channels_of_user (list) - a list contains channels that the user is part of 
    """
    if type(auth_user_id) != int or auth_user_id < 0:
        raise AccessError('User ID is invaild')

    if len(data['channels']) == 0:
        return []

    channels_of_user = []
    for channels in data['channels']:
        if channels['all_members'].count(auth_user_id) > 0:
            channels_of_user.append(channels)
    
    return channels_of_user

def channels_listall_v1(auth_user_id):
    """ 
    Shows all the channels on the list and their details
    
    Arguments: 
        auth_user_id (int) - ID of authorised user

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 

    Return Value:
        data['channels'] (list) - A list contains all the channels stored in the storage
    """
    if type(auth_user_id) != int or auth_user_id < 0:
        raise AccessError('User ID is invaild')

    return data['channels']

def channels_create_v1(auth_user_id, name, is_public):
    """ 
    Create a public/private channel with specified name and owned by user with specified ID
        
    Arguments: 
        auth_user_id (int) - ID of authorised user
        name (str) - Name for the new channel
        is_public (bool) - Flags that indicate the channel is public or private

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid 
        InputError - Occurs when the length of name is too long
        InputError - Occurs when the user with auth_user_id is not registered
        InputError - Occurs when the channel with specified name already exists

    Return Value:
        ｛'channel_id'｝ (dict) - A dictonary that contains the ID of channel created
    """
    global data

    if type(auth_user_id) != int or auth_user_id < 0:
        raise AccessError('User ID is invaild')

    # check if the name of channels is too long
    if len(name) > 20:
        raise InputError('Name is too long')

    found_user = False
    for user in data['users']:
        if user['id'] == auth_user_id:
            found_user = True
            break

    if not found_user:
       raise InputError(f'User with id {auth_user_id} does not exist')  
    
    for channel in data['channels']:
        if channel['name'] == name:
            raise InputError(f'Channel with name {name} already exists')  

    new_channel_id = len(data['channels']) + 1

    data['channels'].append({
        'id': new_channel_id,
        'name': name,
        'user_id': auth_user_id,
        'owner_members' : [auth_user_id],
        'all_members' : [auth_user_id],
        'messages': [],
        'is_public': is_public
    })

    return {
        'channel_id': new_channel_id,
    }
