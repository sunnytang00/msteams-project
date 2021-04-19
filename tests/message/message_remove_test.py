"""Testing the removal of channel and dm messages"""

import pytest
from src.message import message_send_v1, message_remove_v1, message_senddm_v1
from src.dm import dm_create_v1, dm_messages_v1
from src.auth import auth_register_v1
from src.channel import channel_messages_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from tests.helper import helper, clear
from src.channels import channels_create_v1

@clear
def test_message_remove_single(helper):
    """Add and remove a single user's message from a channel"""
    # remove a message in channel
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1

    channel_id = helper.create_channel(1, auth_user_id)
    assert channel_id == 1

    message = "an epic message"

    message_info = message_send_v1(auth_user_id, channel_id, message)
    message_id = message_info.get('message_id')
    assert message_info.get('message_id') == 1

    messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')
    assert len(messages) == 1

    message_remove_v1(auth_user_id, message_id)

    with pytest.raises(InputError) as e:
        messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')
    assert "Start 1 is greater than the total number of messages in the channel" in str(e.value)

    # remove a message in DM
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id2 == 2
    u_ids = [auth_user_id2]
    dm_id = dm_create_v1(auth_user_id, u_ids).get('dm_id')
    assert dm_id == 1

    message_info = message_senddm_v1(auth_user_id, dm_id, message)
    message_id = message_info.get('message_id')
    assert message_id == 2

    message_remove_v1(auth_user_id, message_id)

    with pytest.raises(InputError) as e:
        messages = dm_messages_v1(auth_user_id, dm_id, 1).get('messages')
    assert "Start 1 is greater than the total number of messages in the channel" in str(e.value)

@clear
def test_remove_single_channel_message_in_many(helper):
    """Send 5 messages to a channel and remove the middle one (3rd)"""
    # remove a message in channel
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1

    channel_id = helper.create_channel(1, auth_user_id)
    assert channel_id == 1

    message1 = "test1"
    message2 = "test2"
    message3 = "test3"
    message4 = "test4"
    message5 = "test5"

    message_send_v1(auth_user_id, channel_id, message1)
    message_send_v1(auth_user_id, channel_id, message2)
    message_info = message_send_v1(auth_user_id, channel_id, message3)
    message_send_v1(auth_user_id, channel_id, message4)
    message_send_v1(auth_user_id, channel_id, message5)

    message_id = message_info.get('message_id')
    assert message_info.get('message_id') == 3

    messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')
    assert len(messages) == 5

    message_remove_v1(auth_user_id, message_id)
    messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')

    assert len(messages) == 4

    result = []
    for message in messages:
        result.append(message['message_id'])

    assert result == [1, 2, 4 ,5][::-1]

@clear
def test_message_no_longer_exists(helper):
    """try remove a message that doesn't exist"""
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1

    channel_id = helper.create_channel(1, auth_user_id)
    assert channel_id == 1

    invalid_message_id = 50

    with pytest.raises(InputError) as e: 
        message_remove_v1(auth_user_id, invalid_message_id)
        assert f"Message {invalid_message_id} (based on ID) no longer exists" in str(e.value)

    with pytest.raises(InputError) as e: 
        message_remove_v1(auth_user_id, -1)
        assert f"Message {invalid_message_id} (based on ID) no longer exists" in str(e.value)


@clear
def test_user_is_not_authorised(helper):
    """try removing a message created with auth_user_id with another user that is not a dream owner"""
    message = "an epic message!"
    # remove a message in channel
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1
    not_auth_user_id = helper.register_user(2)
    assert not_auth_user_id == 2

    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    message_info = message_send_v1(auth_user_id, channel_id, message) # send by auth_user
    message_id = message_info.get('message_id') 
    assert message_id == 1

    with pytest.raises(AccessError) as e: 
        message_remove_v1(not_auth_user_id, message_id)
        assert f"Message with message_id {message_id} was not sent by the authorised user making this request" in str(e.value)

    # remove a message in DM
    u_ids = [not_auth_user_id]
    dm_id = dm_create_v1(auth_user_id, u_ids).get('dm_id')
    assert dm_id == 1

    message_info = message_senddm_v1(auth_user_id, dm_id, message)
    message_id = message_info.get('message_id')
    assert message_id == 2

    with pytest.raises(AccessError) as e:
        message_remove_v1(not_auth_user_id, message_id)
        assert f"Message with message_id {message_id} was not sent by the authorised user making this request" in str(e.value)


