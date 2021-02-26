from src.data import data
from src.error import InputError

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
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    #check if the name of channels is too long
    global data
    if len(name) > 20:
        raise InputError('Name is too long')

    new_channel_id = len(data['channels']) + 1
    data['channels'].append({'id': new_channel_id, 'name': name, 'is_public': is_public})
    return {
        'channel_id': new_channel_id,
    }
