"""Messages for channels and DMs

This module demonstrates the sending, removal, editting and sharing of messages as specified by the COMP1531 Major Project specification.
"""

import time
import threading
from src.error import InputError, AccessError
from src.helper import user_is_channel_member, get_channel, get_current_user, user_is_dm_member, \
    remove_message, user_is_Dream_owner, user_is_channel_owner, get_message_ch_id_or_dm_id, edit_message, \
    user_is_dm_owner, format_share_message, get_message, tagged_handlestrs,\
    get_user_from_handlestr, create_notification
from src.data.helper import store_message_channel, store_message_dm, get_message_count, store_notification, update_active_msg_ids
from src.helper import create_message, is_pinned, check_valid_message, get_react_uids, new_message_id, get_dm
from src.data.helper import get_valid_msg_ids, set_pin, set_react, update_user_stats_messages
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
    
    if not user_is_channel_member(channel_id, auth_user_id):
        raise AccessError("Authorised user has not joined the channel")

    handlestrs = tagged_handlestrs(message)
    for handlestr in handlestrs['handle_strs']:
        user = get_user_from_handlestr(handlestr)
        if user and user_is_channel_member(channel_id, user.get('u_id')):
            notification = create_notification(channel_id=channel_id, dm_id=-1, u_id=user.get('u_id'), tagged=True, msgs = message)
            store_notification(notification, user.get('u_id'))

    message = create_message(auth_user_id, message, channel_id=channel_id)
    message_id = message.get('message_id')
    update_active_msg_ids(message_id, 'add')

    store_message_channel(message, channel_id)
    update_user_stats_messages(auth_user_id)
    
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
    output = get_message_ch_id_or_dm_id(message_id)
    channel_id = output.get('channel_id')
    dm_id = output.get('dm_id')

    if not channel_id and not dm_id:
        raise InputError(f"Message {message_id} (based on ID) no longer exists")

    if channel_id:
        if not user_is_channel_owner(channel_id, auth_user_id) and not user_is_Dream_owner(auth_user_id):
            raise AccessError(f"Message with message_id {message_id} was sent by the authorised user making this request")

        remove_message(message_id, channel_id=channel_id)
    else:
        if not user_is_dm_owner(channel_id, auth_user_id) and not user_is_Dream_owner(auth_user_id):
            raise AccessError(f"Message with message_id {message_id} was sent by the authorised user making this request")

        remove_message(message_id, dm_id=dm_id)
        update_active_msg_ids(message_id, 'remove')

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
    output = get_message_ch_id_or_dm_id(message_id)
    channel_id = output.get('channel_id')
    dm_id = output.get('dm_id')

    if not channel_id and not dm_id:
        raise InputError(f"Message {message_id} (based on ID) no longer exists")

    max_length = 1000
    if len(message) > max_length:
        raise InputError("Message is more than 1000 characters")

    if channel_id:
        if not user_is_channel_owner(channel_id, auth_user_id) and not user_is_Dream_owner(auth_user_id):
            raise AccessError(f"Message with message_id {message_id} was sent by the authorised user making this request")

        edit_message(message_id, message=message, channel_id=channel_id)
    else:
        if not user_is_dm_owner(channel_id, auth_user_id) and not user_is_Dream_owner(auth_user_id):
            raise AccessError(f"Message with message_id {message_id} was sent by the authorised user making this request")
        edit_message(message_id, message=message, dm_id=dm_id)

    return {}

def message_senddm_v1(auth_user_id, dm_id, message):
    """Send a message from authorised_user to the DM specified by dm_id. Note: Each message should have it's own unique ID.
     I.E. No messages should share an ID with another message, even if that other message is in a different channel or DM.

    Arguments:
        auth_user_id (int) - The user's id
        message_id (int) - The user's message id
        message (str) - The message contents

    Exceptions:
        InputError - Message is more than 1000 characters
        AccessError - the authorised user is not a member of the DM they are trying to post to

    Return Value:
        Returns dict with message_id on success
    """
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f"auth_user {auth_user_id} is not member of dm {dm_id}")

    max_length = 1000

    if len(message) > max_length:
        raise InputError("message is too long")

    msg_id = get_message_count() + 1
    msg = create_message(auth_user_id, message, dm_id=dm_id)
    store_message_dm(msg, dm_id)
    update_active_msg_ids(msg_id, 'add')
    update_user_stats_messages(auth_user_id)

    return {
        'message_id' : msg_id
    }

def message_share_v1(auth_user_id, og_message_id, message, channel_id, dm_id):
    """og_message_id is the original message. channel_id is the channel that the message is being shared to,
    and is -1 if it is being sent to a DM. dm_id is the DM that the message is being shared to, and is -1
    if it is being sent to a channel. message is the optional message in addition to the shared message,
    and will be an empty string '' if no message is given

    Arguments:
        auth_user_id (int) - The authenticated user's id
        og_message_id (int) - The original message
        channel_id (int) - the channel that the message is being shared to
        dm_id (int) - the DM that he message is being shared to
    
    Exceptions:
        AccessError - the authorised user has not joined the channel or DM they are trying to share the message to

    Return Value:
        Returns shared_message_id on successfully sharing message
    """

    output = get_message_ch_id_or_dm_id(og_message_id)
    og_channel_id = output.get('channel_id')
    og_dm_id = output.get('dm_id')
    og_message = get_message(og_message_id)

    if og_channel_id:
        if not user_is_channel_member(channel_id, auth_user_id):
            raise AccessError(f"the authorised user has not joined the channel or DM they are trying to share the message to")

        # share/send message to DM
        if channel_id == -1:
            pass

        # share/send message to channel
        if dm_id == -1:
            share_message = format_share_message(og_message, message)

            message = create_message(auth_user_id, share_message, channel_id=channel_id)
            store_message_channel(message, channel_id)
            return {
                'shared_message_id': message.get('message_id')
            }

    else:
        # og_message is from a DM
        if not user_is_dm_member(og_dm_id, auth_user_id):
            raise AccessError(f"the authorised user has not joined the channel or DM they are trying to share the message to")

        if channel_id == -1:
            share_message = format_share_message(og_message, message)

            message = create_message(auth_user_id, share_message, channel_id=channel_id)
            store_message_dm(message, dm_id)
            return {
                'shared_message_id': message.get('message_id')
            }

    return {
        'shared_message_id': None
    }

def message_pin_v1(auth_user_id, message_id):
    if message_id not in get_valid_msg_ids():
        raise InputError(f'message with message id {message_id} is not a valid message')
    if is_pinned(message_id):
        raise InputError(f'message with message id {message_id} is already pinned')

    channel_id = get_message_ch_id_or_dm_id(message_id).get('channel_id')
    dm_id = get_message_ch_id_or_dm_id(message_id).get('dm_id')
    if channel_id != None:
        if not user_is_channel_member(channel_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not channel member')
        if not user_is_channel_owner(channel_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not channel owner')
        set_pin(message_id, 'pin', channel_id=channel_id)
    if dm_id != None:
        if not user_is_dm_member(dm_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not dm member')
        if not user_is_dm_owner(dm_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not dm owner')
        set_pin(message_id, 'pin', dm_id=dm_id)
    
def message_unpin_v1(auth_user_id, message_id):
    if message_id not in get_valid_msg_ids():
        raise InputError(f'message with message id {message_id} is not a valid message')
    if not is_pinned(message_id):
        raise InputError(f'message with message id {message_id} is not pinned')

    channel_id = get_message_ch_id_or_dm_id(message_id).get('channel_id')
    dm_id = get_message_ch_id_or_dm_id(message_id).get('dm_id')
    if channel_id != None:
        if not user_is_channel_member(channel_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not channel member')
        if not user_is_channel_owner(channel_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not channel owner')
        set_pin(message_id, 'unpin', channel_id=channel_id)
    if dm_id != None:
        if not user_is_dm_member(dm_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not dm member')
        if not user_is_dm_owner(dm_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not dm owner')
        set_pin(message_id, 'unpin', dm_id=dm_id)
    

def message_react_v1(auth_user_id, message_id, react_id):

    valid_react_id = 1

    if not check_valid_message(message_id):
        raise InputError(f'message_id {message_id} is not a valid message within a channel/dm')
    if react_id != valid_react_id:
        raise InputError(f'react_id {react_id} is not a valid React ID')

    channel_id = get_message_ch_id_or_dm_id(message_id).get('channel_id')
    dm_id = get_message_ch_id_or_dm_id(message_id).get('dm_id')
    if channel_id != None:
        if not user_is_channel_member(channel_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not channel member')
        if auth_user_id in get_react_uids(message_id):
            raise InputError(f'user with id {auth_user_id} has already reacted to message id {message_id} in channel')
        set_react(message_id, auth_user_id, 'react', channel_id=channel_id)

    if dm_id != None:
        if not user_is_dm_member(dm_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not dm member')
        if auth_user_id in get_react_uids(message_id,):
            raise InputError(f'user with id {auth_user_id} has already reacted to message id {message_id} in dm')
        set_react(message_id, auth_user_id, 'react', dm_id=dm_id)


def message_unreact_v1(auth_user_id, message_id, react_id):
    valid_react_id = 1

    if not check_valid_message(message_id):
        raise InputError(f'message_id {message_id} is not a valid message within a channel/dm')
    if react_id != valid_react_id:
        raise InputError(f'react_id {react_id} is not a valid React ID')

    channel_id = get_message_ch_id_or_dm_id(message_id).get('channel_id')
    dm_id = get_message_ch_id_or_dm_id(message_id).get('dm_id')
    if channel_id != None:
        if not user_is_channel_member(channel_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not channel member')
        if auth_user_id not in get_react_uids(message_id):
            raise InputError(f'user with id {auth_user_id} has no active reacts for message id {message_id} in channel')
        set_react(message_id, auth_user_id, 'unreact', channel_id=channel_id)

    if dm_id != None:
        if not user_is_dm_member(dm_id, auth_user_id):
            raise AccessError(f'member with id {auth_user_id} is not dm member')
        if auth_user_id not in get_react_uids(message_id,):
            raise InputError(f'user with id {auth_user_id} has no active reacts for message id {message_id} in channel')
        set_react(message_id, auth_user_id, 'unreact', dm_id=dm_id)

def sendlater(*args, **kwargs):
    auth_user_id = kwargs.get('auth_user_id')
    channel_id = kwargs.get('channel_id')
    message = kwargs.get('message')
    handlestrs = tagged_handlestrs(message)
    for handlestr in handlestrs['handle_strs']:
        user = get_user_from_handlestr(handlestr)
        if user and user_is_channel_member(channel_id, user.get('u_id')):
            notification = create_notification(channel_id=channel_id, dm_id=-1, u_id=user.get('u_id'), tagged=True, msgs = message)
            store_notification(notification, user.get('u_id'))

    message = create_message(auth_user_id, message, channel_id=channel_id)
    message_id = message.get('message_id')
    update_active_msg_ids(message_id, 'add')

    store_message_channel(message, channel_id)


def message_sendlater_v1(auth_user_id, channel_id, message, time_sent):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_channel(channel_id):
        raise InputError(f'Channel ID {channel_id} is not a valid channel')

    if not user_is_channel_member(channel_id, auth_user_id):
        raise AccessError('the authorised user is not a member of the DM they are trying to post to')

    if len(message) > 1000:
        raise InputError('messages is too long')

    if time_sent < int(time.time()):
        raise InputError('Time sent is a time in the past')

    length = time_sent - int(time.time())
    kwargs = {'auth_user_id': auth_user_id, 'channel_id': channel_id, 'message': message}
    t = threading.Timer(length, sendlater, kwargs = kwargs)
    t.start()

    message_id = new_message_id()

    return {'message_id': message_id}

def sendlaterdm(*args, **kwargs):
    auth_user_id = kwargs.get('auth_user_id')
    dm_id = kwargs.get('dm_id')
    message = kwargs.get('message')
    handlestrs = tagged_handlestrs(message)
    for handlestr in handlestrs['handle_strs']:
        user = get_user_from_handlestr(handlestr)
        if user and user_is_dm_member(dm_id, user.get('u_id')):
            notification = create_notification(channel_id=-1, dm_id=-dm_id, u_id=user.get('u_id'), tagged=True, msgs = message)
            store_notification(notification, user.get('u_id'))

    msg_id = get_message_count() + 1
    msg = create_message(auth_user_id, message, dm_id=dm_id)
    
    update_active_msg_ids(msg_id, 'add')
    store_message_dm(msg, dm_id)

def message_sendlaterdm_v1(auth_user_id, dm_id, message, time_sent):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_dm(dm_id):
        raise InputError(f'DM ID {dm_id} is not a valid DM')

    if not user_is_dm_member(dm_id,auth_user_id):
        raise AccessError('the authorised user is not a member of the DM they are trying to post to')

    if len(message) > 1000:
        raise InputError('messages is too long')

    if time_sent < int(time.time()):
        raise InputError('Time sent is a time in the past')

    length = time_sent - int(time.time())
    kwargs = {'auth_user_id': auth_user_id, 'dm_id': dm_id, 'message': message}
    t = threading.Timer(length, sendlaterdm, kwargs = kwargs)
    t.start()

    message_id = new_message_id()

    return {'message_id': message_id}