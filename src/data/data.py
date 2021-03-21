from json import load, JSONDecodeError
from src.config import data_path

data = {
    'users': [

    ],
    'channels': [

    ],
}

try:
    # update dict with stored data
    with open(data_path, 'r') as f:
        stored_data = load(f)

    with open(data_path, 'w') as f:
        data['users'] = stored_data.get('users')
        data['channels'] = stored_data.get('channels')

except (FileNotFoundError, JSONDecodeError) as e:
    # initialise file
    with open(data_path, 'w') as f:
        pass

''' 
Dummy Data for Database

data = {
    'users': [
        { 
        'u_id': 0, #user_id,
        'email': sample_0@something.com                         #email,
        'name_first': first_sample_name_0                       #name_first,
        'name_last': last_sample_name_0                         #name_last,
        'handle_str': first_sample_name_0last_sample_name_0     #handle_str,
        'password': password_0_1324&#!$                            #password
        },
        { 
        'u_id': 1, #user_id,
        'email': sample_1@something.com                         #email,
        'name_first': first_sample_name_1                       #name_first,
        'name_last': last_sample_name_1                         #name_last,
        'handle_str': first_sample_name_1last_sample_name_1     #handle_str,
        'password': password_1_1324&#!$                            #password
        },
    ],
    'channels': [           
        {
        'channel_id': 0,
        'name': Sample_channel_0,
        'owner_members': [
            0,
        ],
        'all_members': [
            0,
            1,
        ],
        'messages': [
            {
                'message_id': 0,
                'u_id': 0,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'is_public': TRUE
        }
    ],
}