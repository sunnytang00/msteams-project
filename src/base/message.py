"""TODO"""

from src.base.error import InputError, AccessError
from src.base.helper import user_is_member, get_channel
from src.data.helper import store_message
from src.base.helper import create_message

def message_send_v1(auth_user_id, channel_id, message):

    channel_data = get_channel(channel_id)

    if len(message) > 1000:
        raise InputError("Message is more than 1000 characters")
    
    if not user_is_member(channel_data, auth_user_id):
        raise AccessError("Authorised user has not joined the channel")

    message = create_message(auth_user_id, channel_id, message)
    store_message(message, channel_id)
    
    return {
        'message_id': message.get('message_id')
    }

def message_remove_v1(auth_user_id, message_id):
    """TODO"""
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    """TODO"""
    return {
    }