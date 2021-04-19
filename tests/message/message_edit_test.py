"""Update a channel or DM message"""

import pytest
from src.message import message_send_v1, message_senddm_v1, message_remove_v1, message_edit_v1
from src.auth import auth_register_v1
from src.dm import dm_create_v1, dm_messages_v1
from src.channel import channel_messages_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from tests.helper import helper, clear
from src.channels import channels_create_v1

@clear
def test_message_edit_single_message(helper):
    """Add and edit a single user's message"""
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1
    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    og_message = "an epic message"
    new_message = "an even more epic message"

    message_info = message_send_v1(auth_user_id, channel_id, og_message)
    message_id = message_info.get('message_id')
    assert message_id == 1

    messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')

    assert messages[0].get('message') == og_message
    message_edit_v1(auth_user_id, message_id, new_message)

    messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages') # get new updated messages
    assert messages[0].get('message') == new_message

    # edit a message in DM
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id2 == 2
    u_ids = [auth_user_id2]
    dm_id = dm_create_v1(auth_user_id, u_ids).get('dm_id')
    assert dm_id == 1

    message_info = message_senddm_v1(auth_user_id, dm_id, og_message)
    message_id = message_info.get('message_id')
    assert message_id == 2

    message_edit_v1(auth_user_id, message_id, new_message)

    messages = dm_messages_v1(auth_user_id, dm_id, 1).get('messages') # get new updated messages
    assert messages[0].get('message') == new_message

@clear
def test_edit_deleted_message(helper):
    """try editting a message that doesn't exist"""
    # edit a message in channel
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1

    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    og_message = "trimesters are super awesome"
    message_info = message_send_v1(auth_user_id, channel_id, og_message)
    message_id = message_info.get('message_id')
    assert message_id == 1

    message_remove_v1(auth_user_id, message_id)

    new_message = "blah blah"
    with pytest.raises(InputError) as e: 
        message_edit_v1(auth_user_id, message_id, new_message)
        assert f"message_id {message_id} refers to a deleted message" in str(e.value)

    # edit a message in DM
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id2 == 2
    u_ids = [auth_user_id2]
    dm_id = dm_create_v1(auth_user_id, u_ids).get('dm_id')
    assert dm_id == 1

    message_info = message_senddm_v1(auth_user_id, dm_id, og_message)
    message_id = message_info.get('message_id')
    assert message_id == 2

    message_remove_v1(auth_user_id, message_id)

    with pytest.raises(InputError) as e: 
        message_edit_v1(auth_user_id, message_id, new_message)
        assert f"message_id {message_id} refers to a deleted message" in str(e.value)

@clear
def test_message_over_1000_char(helper):
    """try editting a message that is over 1000 characters"""
    # edit a message in channel
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1

    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    og_message = "trimesters are super awesome"
    new_message = "a"*1001

    message_info = message_send_v1(auth_user_id, channel_id, og_message)
    message_id = message_info.get('message_id')
    assert message_id == 1

    with pytest.raises(InputError) as e: 
        message_edit_v1(auth_user_id, message_id, new_message)
        assert f"Length of message is over 1000 characters" in str(e.value)

    # edit a message in DM
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id2 == 2
    u_ids = [auth_user_id2]
    dm_id = dm_create_v1(auth_user_id, u_ids).get('dm_id')
    assert dm_id == 1

    message_info = message_senddm_v1(auth_user_id, dm_id, og_message)
    message_id = message_info.get('message_id')
    assert message_id == 2

    with pytest.raises(InputError) as e: 
        message_edit_v1(auth_user_id, message_id, new_message)
        assert f"Length of message is over 1000 characters" in str(e.value)

@clear
def test_user_is_not_authorised(helper):
    """try removing a message created with auth_user_id with another user that is not a dream owner"""
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1
    not_auth_user_id = helper.register_user(2)
    assert not_auth_user_id == 2

    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    message_info = message_send_v1(auth_user_id, channel_id, "an epic message") # send by auth_user
    message_id = message_info.get('message_id') 
    assert message_id == 1

    og_message = "the batmobile"
    new_message = "trucks are cool just like bikes"

    with pytest.raises(AccessError) as e: 
        message_edit_v1(not_auth_user_id, message_id, og_message)
        assert f"Message with message_id {message_id} was not sent by the authorised user making this request" in str(e.value)

    # edit a message in DM
    u_ids = [not_auth_user_id] # even though a member shouldn't be able to edit message of another user in same DM
    dm_id = dm_create_v1(auth_user_id, u_ids).get('dm_id')
    assert dm_id == 1

    message_info = message_senddm_v1(auth_user_id, dm_id, og_message)
    message_id = message_info.get('message_id')
    assert message_id == 2

    message_edit_v1(auth_user_id, message_id, new_message)

    messages = dm_messages_v1(auth_user_id, dm_id, 1).get('messages') # get new updated messages
    assert messages[0].get('message') == new_message

    with pytest.raises(AccessError) as e:
        message_edit_v1(not_auth_user_id, message_id, new_message)
        assert f"Message with message_id {message_id} was not sent by the authorised user making this request" in str(e.value)

