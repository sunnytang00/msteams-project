from src.data import data
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    """ TODO: add docstring
    """

    # TODO: AccessError expection
    global data
    users = data['users']

    found_auth_user_id = False
    found_u_id = False
    for user in users:
        if user['id'] == auth_user_id:
            found_auth_user_id = True
        if user['id'] == u_id:
            found_u_id = True
    
    if not found_auth_user_id or not found_u_id:
        raise InputError('User with ID does not exist')
    
    channels = data['channels']
    for channel in channels:
        if channel['id'] == channel_id:
            channel['all_members'].append(u_id)
            return {}

    raise InputError('Channel with ID does not exist')

def channel_details_v1(auth_user_id, channel_id):
    """ TODO: add docstring
    """
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    """ TODO: add docstring
    """
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    """ 
    Add user as the member of channel with specified ID

    Arguments: 
        auth_user_id (int) - ID of authorised user
        channel_id (int) - ID of the channel

    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid
        AccessError - Occurs when the channel is private 
        InputError - Occurs when the channel_id is invalid
        InputError - Occurs when the channel with id entered is not created
        InputError - Occurs when the channel is private and the user is not owner of it

    Return Value:
        Return nothing
    """
    global data

    if type(auth_user_id) != int or auth_user_id < 0:
        raise AccessError('User ID is invaild')

    if type(channel_id) != int or channel_id < 0:
        raise InputError('Channel ID is invaild')

    found_channel = False
    channels = data['channels']

    for channel in channels:
        if channel['id'] == channel_id:
            found_channel = True
            if not channel['is_public']: 
                raise AccessError('Cannot access the private channel')
            if channel['all_members'].count(auth_user_id) > 0:
                raise InputError('The user is already in the channel')
            
            channel['all_members'].append(auth_user_id)
            break

    if not found_channel:
        raise InputError('Channel with ID {channel_id} does not exist')
    
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }