import threading
import time
from src.error import InputError, AccessError
from src.helper import user_is_Dream_owner, remove_user, get_current_user, get_channel, user_is_channel_member,\
                            tagged_handlestrs, create_notification, get_user_from_handlestr, create_message
from src.data.helper import store_message_standup, update_channel_standup, store_notification, store_message_channel

def standup_finish(*args, **kwargs):
    auth_user_id = kwargs.get('auth_user_id')
    channel_id = kwargs.get('channel_id')
    if get_channel(channel_id):
        standup_data = get_channel(channel_id).get('standup')
        buffered_msgs = standup_data.get('buffer')

        messages = ''
        for msg in buffered_msgs:
            handlestrs = tagged_handlestrs(msg)
            for handlestr in handlestrs['handle_strs']:
                user = get_user_from_handlestr(handlestr)
                if user and user_is_channel_member(channel_id, user.get('u_id')):
                    notification = create_notification(channel_id=channel_id, dm_id=-1, \
                                                        u_id=user.get('u_id'), tagged=True, msgs = '@' + handlestr)
                    store_notification(notification, user.get('u_id'))
            messages += (msg + '\n')
        messages = messages[0:-1]
        
        if standup_data.get('active'):
            message = create_message(auth_user_id, messages, channel_id=channel_id)
            store_message_channel(message, channel_id)

        standup_data['active'] = False
        standup_data['time_finish'] = None
        standup_data['buffer'] = []
        update_channel_standup(channel_id, standup_data)


def standup_start_v1(auth_user_id, channel_id, length):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_channel(channel_id):
        raise InputError(f'Channel ID {channel_id} is not a valid channel')
    
    if not user_is_channel_member(channel_id, auth_user_id):
        raise AccessError('Authorised user is not in the channel')

    if get_channel(channel_id)['standup'].get('active'):
        raise InputError('An active standup is currently running in this channel')
    kwargs = {'auth_user_id': auth_user_id, 'channel_id': channel_id}
    standup_data = get_channel(channel_id).get('standup') 
    standup_data['active'] = True

    t = threading.Timer(length, standup_finish, kwargs = kwargs)
    t.start()
    time_finish = int(time.time()) + length
    standup_data['time_finish'] = time_finish
    update_channel_standup(channel_id, standup_data)
    return {
        'time_finish': time_finish
    }

def standup_active_v1(auth_user_id, channel_id):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_channel(channel_id):
        raise InputError(f'Channel ID {channel_id} is not a valid channel')

    standup_data = get_channel(channel_id).get('standup')
    return {'is_active': standup_data.get('active'), 'time_finish': standup_data.get('time_finish')}

def standup_send_v1(auth_user_id, channel_id, message):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_channel(channel_id):
        raise InputError(f'channel_id {channel_id} does not refer to a valid channel')

    if len(message) > 1000:
        raise InputError('messages is too long')

    if not user_is_channel_member(channel_id, auth_user_id):
        raise AccessError(f'auth_user {auth_user_id} does not member of channel {channel_id}')

    standup = get_channel(channel_id).get('standup') 

    if not standup['active']:
        raise InputError('An active standup is not currently running in this channel')
    
    user = get_current_user(auth_user_id)
    handlestr = user.get('handle_str')
    msgs = handlestr + ': ' + message
    store_message_standup(msgs, channel_id)