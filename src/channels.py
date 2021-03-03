from src.data import data
from src.error import InputError, AccessError

def channels_list_v1(auth_user_id):
    """ TODO: add docstring
    """
    if type(auth_user_id) != int or auth_user_id < 0:
        raise AccessError('User ID is invaild')

    if len(data['channels']) == 0:
        return {}

    channels_of_user = []
    for channels in data['channels']:
        if channels['user_id'] == auth_user_id:
            channels_of_user.append(channels)
    
    return channels_of_user

def channels_listall_v1(auth_user_id):
    """ TODO: add docstring
    """
    if type(auth_user_id) != int or auth_user_id < 0:
        raise AccessError('User ID is invaild')

    return data['channels']

def channels_create_v1(auth_user_id, name, is_public):
    """ TODO: add docstring
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
        'member' : [auth_user_id],
        'is_public': is_public
    })

    return {
        'channel_id': new_channel_id,
    }
