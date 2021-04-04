import pytest
from src.base.message import message_send_v1, message_remove_v1
from src.base.auth import auth_register_v1
from src.base.channel import channel_messages_v1
from src.base.other import clear_v1
from src.base.error import InputError, AccessError
from tests.helper import helper, clear
from src.base.channels import channels_create_v1

@clear
def test_message_remove_single(helper):
    """Add and remove a single user's message"""
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1

    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    message_info = message_send_v1(auth_user_id, channel_id, "an epic message")
    message_id = message_info.get('message_id')
    assert message_info.get('message_id') == 1

    messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')
    assert len(messages) == 1

    message_remove_v1(auth_user_id, message_id)

    with pytest.raises(InputError) as e:
        messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')
    assert "Start 1 is greater than the total number of messages in the channel" in str(e.value)

@clear
def test_message_no_longer_exists(helper):
    """try remove a message that doesn't exist"""
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1

    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    message_id = 50

    with pytest.raises(InputError) as e: 
        message_remove_v1(auth_user_id, message_id)
        assert f"Message {message_id} (based on ID) no longer exists" in str(e.value)

@clear
def test_user_is_authorised(helper):
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

    with pytest.raises(AccessError) as e: 
        message_remove_v1(not_auth_user_id, message_id)
        assert f"Message with message_id {message_id} was not sent by the authorised user making this request" in str(e.value)
