"""Share a message to a channel or DM"""

import pytest
from src.message import message_send_v1, message_senddm_v1, message_share_v1
from src.dm import dm_create_v1, dm_messages_v1
from src.auth import auth_register_v1
from src.channel import channel_messages_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from tests.helper import helper, clear
from src.channels import channels_create_v1

@clear
def test_share_channel(helper):
    """Add and remove a single user's message from a channel"""
    # no optional message
    auth_user_id = helper.register_user(1)

    channel_id = helper.create_channel(1, auth_user_id)

    assert auth_user_id == 1
    assert channel_id == 1

    og_message = "I like shrimps"

    message_info = message_send_v1(auth_user_id, channel_id, og_message)
    og_message_id = message_info.get('message_id')

    assert og_message_id == 1

    optional_message = ''

    dm_id = -1
    message_info = message_share_v1(auth_user_id, og_message_id, optional_message, channel_id, dm_id)
    shared_message_id = message_info.get('shared_message_id')
    assert shared_message_id ==  2

    channel_messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')
    shared_message = channel_messages[1]
    shared_message.get('channel_id') == 2

    expected = f'{optional_message}\n\n"""\n{og_message}\n"""'
    assert channel_messages[0].get('message') == expected

    # optional message

@clear
def test_share_dm(helper):
    """Add and remove a single user's message from a dm"""
    # no optional message
    auth_user_id = helper.register_user(1)

    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')
    assert auth_user_id == 1
    assert dm_id == 1

    og_message = "I like shrimps"

    message_info = message_senddm_v1(auth_user_id, dm_id, og_message)
    og_message_id = message_info.get('message_id')

    assert og_message_id == 1

    optional_message = ''

    channel_id = -1
    message_info = message_share_v1(auth_user_id, og_message_id, optional_message, channel_id, dm_id)
    shared_message_id = message_info.get('shared_message_id')
    assert shared_message_id ==  2

    dm_messages = dm_messages_v1(auth_user_id, dm_id, 0).get('messages')

    expected = f'{optional_message}\n\n"""\n{og_message}\n"""'
    assert dm_messages[0].get('message') == expected

    #optional message
    optional_message = '1'
    message_info = message_share_v1(auth_user_id, og_message_id, optional_message, channel_id, dm_id)
    shared_message_id = message_info.get('shared_message_id')
    assert shared_message_id == 3
    dm_messages = dm_messages_v1(auth_user_id, dm_id, 0).get('messages')
    
    expected = f'{optional_message}\n\n"""\n{og_message}\n"""'
    assert dm_messages[0].get('message') == expected

@clear
def test_user_is_not_member_dm(helper):
    auth_user_id = helper.register_user(1)
    u_id = helper.register_user(2)

    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    og_message = "I like shrimps"

    message_info = message_senddm_v1(auth_user_id, dm_id, og_message)
    og_message_id = message_info.get('message_id')

    optional_message = ''

    channel_id = -1
    with pytest.raises(AccessError) as e:
        message_share_v1(u_id, og_message_id, optional_message, channel_id, dm_id)
        assert f"the authorised user has not joined the channel or DM they are trying to share the message to" in str(e)

@clear
def test_user_is_not_member_channel(helper):
    auth_user_id = helper.register_user(1)
    u_id = helper.register_user(2)

    channel_id = helper.create_channel(1, auth_user_id)

    og_message = "I like shrimps"

    message_info = message_send_v1(auth_user_id, channel_id, og_message)
    og_message_id = message_info.get('message_id')

    optional_message = ''

    dm_id = -1
    with pytest.raises(AccessError) as e:
        message_share_v1(u_id, og_message_id, optional_message, channel_id, dm_id)
        assert f"the authorised user has not joined the channel or DM they are trying to share the message to" in str(e)
