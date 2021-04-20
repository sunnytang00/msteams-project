from src.config import data_path
import json
from datetime import timezone, datetime

""" 
Dummy Data for Database

data = {
    'users': [
        { 
            'u_id': 1,                                              
            'email': harrypotter@gmail.com,                         
            'name_first': Harry,                       
            'name_last': Potter,                         
            'handle_str': harrypotter,     
            'password': password_1_1324&#!$,
            'permission_id': 1,
            'notifications' : [],
            'session_list': [123e4567-e89b-12d3-a456-426614174000],
            'profile_img_url': http//localhost:8080/static/phototest.jpg
        },
        { 
            'u_id': 2,                                              
            'email': bobsmith@gmail.com,                         
            'name_first': Bob,                       
            'name_last': Smith,                         
            'handle_str': bobsmith,    
            'password': password_2_1324&#!$,
            'permission_id': 2,
            'notifications' : []
            'session_list': [],
            'profile_img_url': http//localhost:8080/static/phototest.jpg
        },
    ],
    'channels': [           
        {
            'channel_id': 1,
            'name': Sample_channel_1,
            'owner_members': [
                { 
                    'u_id': 1,                                              
                    'email': harrypotter@gmail.com,                        
                    'name_first': Harry,                       
                    'name_last': Potter,                         
                    'handle_str': harrypotter,    
                    'password': password_1_1324&#!$,
                    'permission_id': 1,
                    'session_list': [123e4567-e89b-12d3-a456-426614174000]
                },
            ],
            'all_members': [
                { 
                    'u_id': 1,                                              
                    'email': harrypotter@gmail.com,                        
                    'name_first': Harry,                       
                    'name_last': Potter,                         
                    'handle_str': harrypotter,    
                    'password': password_1_1324&#!$,
                    'permission_id': 1,                        
                    'session_list': [123e4567-e89b-12d3-a456-426614174000]
                },
                { 
                    'u_id': 2,                                              
                    'email': bobsmith@gmail.com,                         
                    'name_first': Bob,                      
                    'name_last': Smith,                         
                    'handle_str': bobsmith,     
                    'password': password_2_1324&#!$,                         
                    'permission_id': 2,                        
                    'session_list': []
                },
            ],
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                    'reacts' : [{'react_id' : 1,
                        'u_ids' : [],
                        'is_this_user_reacted' : False
                            }],
                    'is_pinned' : False
                }
            ],
            'is_public': TRUE,
        }
    ],
    'dms': [
        {
            'auth_user_id': 1,
            'dm_id': 1,
            'u_ids': [1, 2]
            'dm_name': "bobsmith, harrypotter",
            'messages': []
        }
    ],

    'user_count': 2,
    'message_count': 1,
    'channel_count': 1,
    'dm_count': 1,
    'owner_count': 1,
    'valid_msg_ids': [1],
}
"""

def save(data) -> None:
    """Dumps data to data.json"""
    with open(data_path, 'w') as f:
        json.dump(data, f)

def clear_data() -> None:
    """ Resets the internal data of the application to it's initial state
    
    Return Value:
        Returns None on clearing of data
    """

    # initialise keys in data
    cleared_data = {
        'users': [],
        'channels': [],
        'dms': [],
        'user_count': 0,
        'channel_count': 0,
        'message_count': 0,
        'dm_count': 0,
        'owner_count' : 0,
        'valid_msg_ids' : [],
        'dreams_messages_sent' : []
    }

    save(cleared_data)

def get_data() -> dict:
    """Get data stored on data storage

    Return Value:
        Returns data (dict): data stored on the data storage
    """

    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        # initialise data before reading
        clear_data()
        with open(data_path, 'r') as f:
            data = json.load(f)

    return data

def get_user_count() -> int:
    return get_data().get('user_count')

def get_channel_count() -> int:
    return get_data().get('channel_count')

def get_message_count() -> int:
    return get_data().get('message_count')

def get_dm_count() -> int:
    return get_data().get('dm_count')

def get_owner_count() -> int:
    return get_data().get('owner_count')

def get_user_index(u_id: int) -> int:
    """Get the index of the user in users list

    Return Value:
        Returns index on all conditions
    """
    data = get_data()
    users = get_users()
    for idx in range(len(users)-1):
        if data['users'][idx]['u_id'] == u_id:
            return idx
    return -1

def get_channel_index(channel_id: int) -> int:
    """Get the index of the channel in channels list

    Return Value:
        Returns index on all conditions
    """

    data = get_data()
    channels = get_channels()
    for idx in range(len(channels)-1):
        if data['channels'][idx]['channel_id'] == channel_id:
            return idx
    return -1

def get_message_index(message_id: int, channel_idx=None, dm_idx=None) -> int:
    """Get the index of the user in users list

    Return Value:
        Returns index on all conditions
    """
    data = get_data()
    channels = get_channels()
    if channel_idx or channel_idx == 0:
        for channel in channels:
            for idx in range(len(channel['messages'])-1):
                if channel['messages'][idx].get('message_id') == message_id:
                    return idx

    elif dm_idx:
        for idx in range(len(data)-1):
            if data['dms'][dm_idx]['messages'][idx].get('message_id') == message_id:
                return idx
    return -1

def get_dm_index(dm_id: int) -> int:
    """Get the index of a dm in dms

    Return Value:
        Returns index on all conditions
    """
    data = get_data()
    dms = get_dms()
    for idx in range(len(dms)-1):
        if data['dms'][idx]['dm_id'] == dm_id:
            return idx
    return -1

def get_session_id_index(u_id_idx: int, session_id: str) -> int:
    """Get the index of the user's session_id in session_list

    Return Value:
        Returns index on all conditions
    """
    data = get_data()
    user = data['users'][u_id_idx]
    for idx in range(len(user['session_list'])):
        if user['session_list'][idx] == session_id:
            return idx
    return -1

def get_users() -> list:
    """Get list of users from data storage
    
    Return Value:
        Returns list of users on all conditions
    """
    return get_data().get('users')

def get_channels() -> list:
    """Get list of channel from data storage
    
    Return Value:
        Returns list of channels on all conditions
    """
    return get_data().get('channels')

def get_dms() -> list:
    """ Get list of dms from data storage

    Return Value:
        Returns list of dms on all conditions
    """
    return get_data().get('dms')


def get_reset_code(u_id: int) -> str:
    """ Get a user's reset code

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    return data['users'][idx]['reset_code']


def store_message_channel(message: dict, channel_id: int) -> None:
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['messages'].append(message)
    data['message_count'] += 1
    
    save(data)

def store_message_dm(message: dict, dm_id: int) -> None:
    """store message sent to dm on the data storage

    Arguments:
        message (dict) : dictionary contains message and some information of it
        dm_id (int) : id of dm

    Return Value:
        Returns None on all conditions

    """
    data = get_data()
    idx = get_dm_index(dm_id)

    data['dms'][idx]['messages'].append(message)
    data['message_count'] += 1

    save(data)

def store_message_standup(message: str, channel_id: int) -> None:
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['standup']['buffer'].append(message)
    
    save(data)

def store_user(user: dict) -> None:
    """store the data of user on data storage
    
    Arguments:
        user (dict) - a user

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    data.get('users').append(user)
    data['user_count'] += 1

    save(data)

def store_session_id(u_id: int, session_id: str) -> None:
    """Update the user's session id
    
    Arguments:
        u_id (int) - The user's id
        session_id (str) - The user's session id

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['session_list'].append(session_id)

    save(data)

def remove_session_id(u_id: int, session_id: str) -> bool:
    """remove the user's session id
    
    Arguments:
        u_id (int) - The user's id
        session_id (str) - The user's session id

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    u_id_idx = get_user_index(u_id)
    session_idx = get_session_id_index(u_id_idx, session_id) 
    if session_idx == -1:
        # didn't find session_id
        return False

    del data['users'][u_id_idx]['session_list'][session_idx]

    save(data)
    return True

def update_name_first(u_id: int, name_first: str) -> None:
    """Update the user's first name
    
    Arguments:
        u_id (int) - The user's id
        name_first (str) - The user's last name

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['name_first'] = name_first

    save(data)

def update_name_last(u_id: int, name_last: str) -> None:
    """Update the user's last name
    
    Arguments:
        u_id (int) - The user's id
        name_last (str) - The user's last name

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['name_last'] = name_last

    save(data)

def update_email(u_id: int, email: str) -> None:
    """Update the user's email
    
    Arguments:
        u_id (int) - The user's id
        email (str) - The user's handle

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['email'] = email

    save(data)

def update_handle_str(u_id: int, handle_str: str) -> None:
    """Update the user's handle (i.e. display name)
    
    Arguments:
        u_id (int) - The user's id
        handle_str (str) - The user's handle

    Return Value:
        Returns None if updated user's handle_str successfully
    """
    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['handle_str'] = handle_str 

    save(data)

def update_profile_img_url(u_id: int, url: str) -> None:
    """Update the user's img_url (the photo displayed)
    
    Arguments:
        u_id (int) - The user's id
        url (str) - url being used for accessing the photo
    Return Value:
        Returns None if updated user's url successfully
    """
    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['profile_img_url'] = url

    save(data)

def store_channel(channel: dict) -> bool:
    """Store the data of channel on data storage

    Arguments:
        channel (list): List of channel

    Return Value:
        True if the channel data stored successfully
        False if fail to store channel data
    """
    data = get_data()

    data['channels'].append(channel)
    data['channel_count'] += 1

    save(data)
    if get_channels() == data["channels"]:
        return True
    return False

def append_channel_all_members(channel_id: int, user: dict) -> None:
    """Append a user to channel all members

    Arguments:
        channel_id (int) - id of channel
        user (dict) - the user's data

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['all_members'].append(user)

    save(data)

def append_channel_owner_members(channel_id: int, user: dict) -> None:
    """Append a user to channel owner members

    Arguments:
        channel_id (int) - id of channel
        user (dict) - the user's data

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['owner_members'].append(user)

    save(data)

def update_owner_members(channel_id: int, owner_members: list) -> None:
    """Update the owners users of a channel

    Arguments:
        channel_id (int) - id of channel
        owner_members (list) - the users that are owners of a channel

    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['owner_members'] = owner_members 

    save(data)

def update_all_members(channel_id : int, all_members: list) -> None:
    """Update the member users of a channel

    Arguments:
        channel_id (int) - id of channel
        all_members (list) - the users that are members of a channel

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['all_members'] = all_members 

    save(data)

def update_permission_id(auth_user_id : int, permission_id: int) -> None:
    """Update the permission id of a user

    Arguments:
        auth_user_id (int) - id of user
        permission_id (int) - new permission id assigned to user

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_user_index(auth_user_id)
    data['users'][idx]['permission_id'] = permission_id

    save(data)

def update_password(auth_user_id: int, password: str) -> None:
    """Update a users password

    Arguments:
        auth_user_id (int) - id of user
        passwordl (str) - the new password of a user

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_user_index(auth_user_id)
    data['users'][idx]['password'] = password

    save(data)

def update_dm_list(dms: list) -> None:
    data = get_data()
    data['dms'] = dms

    save(data)

def update_dm_users(dm_users: list, dm_id: int) -> None:
    data = get_data()
    idx = get_dm_index(dm_id)
    data['dms'][idx]['u_ids'] = dm_users

    save(data)
    
def update_channel_standup(channel_id: int, standup: dict) -> None:
    data = get_data()
    idx = get_channel_index(channel_id)

    data['channels'][idx]['standup'] = standup

    save(data)

def store_dm(dm: dict) -> None:
    """store the dm in storage
    
    Arguments:
        dm (dict) - a dm

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    data.get('dms').append(dm)

    data['dm_count'] += 1
    save(data)

def store_reset_code(u_id: int, reset_code: str) -> None:
    """store a user's reset code
    
    Arguments:
        u_id (int) - the user's id

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['reset_code'] = reset_code
    save(data)

def remove_reset_code(u_id: int) -> None:
    """remove/reset a user's reset code
    
    Arguments:
        u_id (int) - the user's id

    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_user_index(u_id)

    data['users'][idx]['reset_code'] = ""
    save(data)

def update_owner_count(owner_count : int) -> None:
    """ update the count of owner 

    Arguments:
        owner_count (int) - new count for owner
    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    data['owner_count'] = owner_count
    save(data)

def update_user_count(user_count: int) -> None:
    """ update the count of user 

    Arguments:
        user_count (int) - new count for user
    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    data['owner_count'] = user_count
    save(data)

def update_removed_flag(auth_user_id : int, flag: bool) -> None:
    """ update the removed flag of user 

    Arguments:
        auth_user_id (int) - id of user
        flag (bool) - True if user being removed, False if not
    Return Value:
        Returns None on all conditions
    """

    data = get_data()
    idx = get_user_index(auth_user_id)
    data['users'][idx]['removed'] = flag
    save(data)

def update_user_all_channel_message(auth_user_id : int, ch_id: dict, message: str) -> None:
    """ update the contents of msg sent by a user in channel

    Arguments:
        auth_user_id (int) - id of user
        ch_id (int) - id of channel
        message (str) - new message 
    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_channel_index(ch_id)
    msgs = data['channels'][idx]['messages']
    i = 0
    while i < len(msgs):
        if msgs[i]['u_id'] == auth_user_id:
            msgs[i]['message'] = message
        i += 1
    data['channels'][idx]['messages'] = msgs
    save(data)

def update_user_all_dm_message(auth_user_id: int, dm_id: int, message: str) -> None:
    """ update the contents of msg sent by a user in dm

    Arguments:
        auth_user_id (int) - id of user
        dm_id (int) - id of dm
        message (str) - new message 
    Return Value:
        Returns None on all conditions
    """
    data = get_data()
    idx = get_dm_index(dm_id)
    msgs = data['dms'][idx]['messages']
    i = 0
    while i < len(msgs):
        if msgs[i]['u_id'] == auth_user_id:
            msgs[i]['message'] = message
        i += 1
    data['dms'][idx]['messages'] = msgs
    save(data)

def update_message(message_id: int, channel_id = None, dm_id = None, message = None) -> None:
    """ remove or edit a message in a channel or dm

    Arguments:
        message_id (int) - id of a message
        channel_id (optional) (int) - id of a channel
        dm_id (optional) (int) - id of a dm
        message (optional) (str) - a message

    Return Value:
        Returns None on all conditions
    """
    data = get_data()

    if channel_id:
        channel_idx = get_channel_index(channel_id)
        message_idx = get_message_index(message_id, channel_idx=channel_idx)
        if not message:
            # no message given so we want to delete a message
            del data['channels'][channel_idx]['messages'][message_idx]
        else:
            # message given so we want to edit the message
            data['channels'][channel_idx]['messages'][message_idx]['message'] = message
    else:
        dm_idx = get_dm_index(dm_id)
        message_idx = get_message_index(message_id, dm_idx=dm_idx)
        if not message:
            del data['dms'][dm_idx]['messages'][message_idx]
        else:
            data['dms'][dm_idx]['messages'][message_idx]['message'] = message

    save(data)

def store_notification(notification: dict, u_id: int) -> None:
    
    data = get_data()
    user_idx = get_user_index(u_id)

    data['users'][user_idx]['notifications'].append(notification)

    save(data)

def get_valid_msg_ids() -> list:
    return get_data().get('valid_msg_ids')

def update_active_msg_ids(msg_id: int, method: str) -> None:
    data = get_data()
    if method == 'add':
        data['valid_msg_ids'].append(msg_id)
    if method == 'remove':
        data['valid_msg_ids'].remove(msg_id)
    save(data)

def set_pin(message_id: int, to_pin: str, channel_id = None, dm_id = None) -> None:
    data = get_data()
    if channel_id:
        channel_idx = get_channel_index(channel_id)
        message_idx = get_message_index(message_id, channel_idx=channel_idx)
        if to_pin == 'pin':
            data['channels'][channel_idx]['messages'][message_idx]['is_pinned'] = True
        if to_pin == 'unpin':
            data['channels'][channel_idx]['messages'][message_idx]['is_pinned'] = False
    else:
        dm_idx = get_dm_index(dm_id)
        message_idx = get_message_index(message_id, dm_idx=dm_idx)
        if to_pin == 'pin':
            data['dms'][dm_idx]['messages'][message_idx]['is_pinned'] = True
        if to_pin == 'unpin':
            data['dms'][dm_idx]['messages'][message_idx]['is_pinned'] = False

    save(data)

def set_react(message_id: int, auth_user_id: int, to_react: str, channel_id = None, dm_id = None) -> list:
    data = get_data()
    if channel_id:
        channel_idx = get_channel_index(channel_id)
        message_idx = get_message_index(message_id, channel_idx=channel_idx)
        if to_react == 'react':
            data['channels'][channel_idx]['messages'][message_idx]['reacts'][0]['u_ids'].append(auth_user_id)
        if to_react == 'unreact':
            data['channels'][channel_idx]['messages'][message_idx]['reacts'][0]['u_ids'].remove(auth_user_id)

    else:
        dm_idx = get_dm_index(dm_id)
        message_idx = get_message_index(message_id, dm_idx=dm_idx)
        if to_react == 'react':
            data['dms'][dm_idx]['messages'][message_idx]['reacts'][0]['u_ids'].append(auth_user_id)
        if to_react == 'unreact':
            data['dms'][dm_idx]['messages'][message_idx]['reacts'][0]['u_ids'].remove(auth_user_id)
    
    save(data)

"""
def store_user_stats(auth_user_id : int, stats: dict) -> None:
    data = get_data()
    idx = get_user_index(auth_user_id)
    data['users'][idx]
    data['user_statistics'].append(stats)
    save(data)
"""

def update_user_stats_channels(auth_user_id: int, change: str) -> None:
    # could combine these into one function but i think its easier to understand if i separate
    data = get_data()
    idx = get_user_index(auth_user_id)
    if change == 'add':
        data['users'][idx]['user_stats']['channels_joined'][0]['num_channels_joined'] += 1
        timenow = datetime.utcnow()
        timestamp = int(timenow.replace(tzinfo=timezone.utc).timestamp())
        data['users'][idx]['user_stats']['channels_joined'][0]['time_stamp'].append(timestamp)

    if change == 'remove':
        data['users'][idx]['user_stats']['channels_joined'][0]['num_channels_joined'] -= 1
        timenow = datetime.utcnow()
        timestamp = int(timenow.replace(tzinfo=timezone.utc).timestamp())
        data['users'][idx]['user_stats']['channels_joined'][0]['time_stamp'].append(timestamp)

    save(data)

def update_user_stats_dms(auth_user_id: int, change: str):
    data = get_data()
    idx = get_user_index(auth_user_id)
    if change == 'add':
        data['users'][idx]['user_stats']['dms_joined'][0]['num_dms_joined'] += 1
        timenow = datetime.utcnow()
        timestamp = int(timenow.replace(tzinfo=timezone.utc).timestamp())
        data['users'][idx]['user_stats']['dms_joined'][0]['time_stamp'].append(timestamp)

    if change == 'remove':
        data['users'][idx]['user_stats']['dms_joined'][0]['num_dms_joined'] -= 1
        timenow = datetime.utcnow()
        timestamp = int(timenow.replace(tzinfo=timezone.utc).timestamp())
        data['users'][idx]['user_stats']['dms_joined'][0]['time_stamp'].append(timestamp)

    save(data)

def update_user_stats_messages(auth_user_id: int):
    data = get_data()
    idx = get_user_index(auth_user_id)
    data['users'][idx]['user_stats']['messages_sent'][0]['num_messages_sent'] += 1
    timenow = datetime.utcnow()
    timestamp = int(timenow.replace(tzinfo=timezone.utc).timestamp())
    data['users'][idx]['user_stats']['messages_sent'][0]['time_stamp'].append(timestamp)
    save(data)

def get_user_stats(auth_user_id: int) -> dict:
    data = get_data()
    idx = get_user_index(auth_user_id)
    return data['users'][idx]['user_stats']

def store_involvement_rate(auth_user_id: int, involvement_rate) -> None:
    data = get_data()
    idx = get_user_index(auth_user_id)
    data['users'][idx]['user_stats']['involvement_rate'] = involvement_rate
    save(data)
