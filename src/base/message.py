"""TODO"""
import time
from src.base.error import InputError, AccessError
from src.base.helper import user_is_member, get_channel, get_current_user, user_is_dm_member, remove_message, user_is_Dream_owner, user_is_owner, get_message_channel_id, edit_message
from src.data.helper import store_message, store_message_dm, get_message_count
from src.base.helper import create_message

def message_send_v1(auth_user_id, channel_id, message):
    """Send a message from authorised_user to the channel specified by channel_id.
    Note: Each message should have it's own unique ID. I.E. No messages should share
    an ID with another message, even if that other message is in a different channel.

    Arguments:
        auth_user_id (int) - The user's id
        channel_id (int) - The id of the channel the message was sent in
        message (str) - The message contents

    Exceptions:
        InputError - Message is more than 1000 characters
        AccessError - The authorised user has not joined the channel they are trying to post to

    Return Value:
        Returns message_id on successfully sending a message
    """

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
    """Given a message_id for a message, this message is removed from the channel/DM

    Arguments:
        auth_user_id (int) - The user's id
        message_id (int) - The user's message id

    Exceptions:
        InputError - Message (based on ID) no longer exists
        AccessError when none of the following are true:
            - Message with message_id was sent by the authorised user making this request
            - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

    Return Value:
        Returns empty dict on successfully removing a message
    """
    channel_id = get_message_channel_id(message_id)
    channel = get_channel(channel_id)
    if not user_is_owner(channel, auth_user_id) and not user_is_Dream_owner(auth_user_id):
        raise AccessError(f"Message with message_id {message_id} was sent by the authorised user making this request")

    if not remove_message(message_id):
        raise InputError(f"Message {message_id} (based on ID) no longer exists")

    return {}

def message_edit_v1(auth_user_id, message_id, message):
    """Given a message, update its text with new text. If the new message is an empty string, the message is deleted.

    Arguments:
        auth_user_id (int) - The user's id
        message_id (int) - The user's message id
        message (str) - The message contents

    Exceptions:
        InputError - Length of message is over 1000 characters
        InputError - message_id refers to a deleted message
        AccessError when none of the following are true:
            - Message with message_id was sent by the authorised user making this request
            - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

    Return Value:
        Returns empty dict on successfully editing a message
    """
    channel_id = get_message_channel_id(message_id)
    channel = get_channel(channel_id)

    if not user_is_owner(channel, auth_user_id) and not user_is_Dream_owner(auth_user_id):
        raise AccessError(f"Message with message_id {message_id} was sent by the authorised user making this request")

    if len(message) > 1000:
        raise InputError("Message is more than 1000 characters")

    if not edit_message(message_id, message):
        raise InputError(f"message_id {message_id} refers to a deleted message")

    return {}

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
