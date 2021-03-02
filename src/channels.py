from src.data import data
from src.error import InputError,AccessError

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    if (type(auth_user_id) != int or auth_user_id < 0):
        raise AccessError('User ID is invaild')


    return data['channels']

def channels_create_v1(auth_user_id, name, is_public):
    #check if the name of channels is too long
    global data

    if(type(auth_user_id) != int or auth_user_id < 0):
        raise AccessError('User ID is invaild')

    if len(name) > 20:
        raise InputError('Name is too long')

    found_user = False
    found_duplicate_name = False
    for user in data['users']:
        if user['id'] == auth_user_id:
            found_user = True
            break
    
    for channel in data['channels']:
        if len(data['channels']) > 0:
            if channel['name'] == name:
                found_duplicate_name = True
                break
    if found_user == False:
       raise InputError(f'User with id {auth_user_id} does not exist')  
    if found_duplicate_name == True:
        raise InputError(f'Channel with name {name} already exists')  
    new_channel_id = len(data['channels']) + 1
    data['channels'].append({'id': new_channel_id, 'name': name, 'uesr_id': auth_user_id, 'is_public': is_public})
    return {
        'channel_id': new_channel_id,
    }
