"""TODO"""
import time
from src.base.error import InputError, AccessError
from src.base.helper import user_is_member, get_channel, get_current_user, user_is_dm_member, remove_message, user_is_Dream_owner, user_is_owner, get_message_channel_id
from src.data.helper import store_message, store_message_dm, get_message_count
from src.base.helper import create_message

def message_send_v1(auth_user_id, channel_id, message):

   # channel_data = get_channel(channel_id)

    if len(message) > 1000:
        raise InputError("Message is more than 1000 characters")
    
    if not user_is_member(channel_id, auth_user_id):
        raise AccessError("Authorised user has not joined the channel")

    message = create_message(auth_user_id, channel_id, message)
    store_message(message, channel_id)
    
    return {
        'message_id': message.get('message_id')
    }

def message_remove_v1(auth_user_id, message_id):
    """TODO"""
    channel_id = get_message_channel_id(message_id)
    channel = get_channel(channel_id)
    if not user_is_owner(channel, auth_user_id) and not user_is_Dream_owner(auth_user_id):
        raise AccessError(f"Message with message_id {message_id} was sent by the authorised user making this request")

    if not remove_message(message_id):
        raise InputError(f"Message {message_id} (based on ID) no longer exists")

    return {}

def message_edit_v1(auth_user_id, message_id, message):
    """TODO"""
    return {
    }

def message_senddm_v1(auth_user_id, dm_id, message):
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f"auth_user {auth_user_id} is not member of dm {dm_id}")

    max_length = 1000

    if len(message) > max_length:
        raise InputError("message is too long")

    msg_id = get_message_count() + 1
    time_created = int(time.time())

    msg = {'message_id' : msg_id,
            'u_id' : auth_user_id,
            'message': message,
            'time_created' : time_created
    }
    store_message_dm(msg, dm_id)

    return {
        'message_id' : msg_id
    }

#def message_share_v1():
