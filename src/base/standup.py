import threading
import time
from src.base.error import InputError, AccessError
from src.base.helper import user_is_Dream_owner, remove_user, get_current_user, get_channel, user_is_channel_member
from src.data.helper import store_message_standup, update_channel_startup

def startup_finish(*args, **kwargs):
    channel_id = kwargs.get('channel_id')
    startup_data = get_channel(channel_id).get('startup')
    buffered_msgs = startup_data.get('buffer')
    for msg in buffered_msgs:
        

def standup_start_v1(auth_user_id, channel_id, length):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_channel(channel_id):
        raise InputError(f'Channel ID {channel_id} is not a valid channel')
    
    if not user_is_channel_member(channel_id, auth_user_id):
        raise AccessError('Authorised user is not in the channel')

    if get_channel(channel_id)['startup'].get('active'):
        raise InputError('An active standup is currently running in this channel')

    kwargs = {'auth_user_id': auth_user_id, 'channel_id': channel_id}
    startup_data = get_channel(channel_id).get('startup') 
    startup_data.get('active') = True
    update_channel_startup(channel_id, startup_data)
    threading.timer(length, startup_finish, kwargs = kwargs)
    time_finish = int(time.time()) + length
    return {
        'time_finish': time_finish
    }

def standup_send_v1(auth_user_id, channel_id, message):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_channel(channel_id):
        raise InputError(f'channel_id {channel_id} does not refer to a valid channel')

    if len(message) > 1000:
        raise InputError('messages is too long')

    if not user_is_channel_member(channel_id, auth_user_id):
        raise AccessError(f'auth_user {auth_user_id} does not member of channel {channel_id}')

    '''
    standup = get_standup(channel_id)
    if not standup['active']:
        raise InputError('An active standup is not currently running in this channel')
    '''
    user = get_current_user(auth_user_id)
    handlestr = user.get('handle_str')
    msgs = handlestr + ': ' + message
    store_message_standup(msgs, channel_id)