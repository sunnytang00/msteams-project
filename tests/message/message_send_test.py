import pytest
from src.base.message import message_send_v1
from src.base.auth import auth_login_v1, auth_register_v1
from src.base.other import clear_v1
from src.base.error import InputError, AccessError
from tests.helper import helper, clear
from src.base.channels import channels_create_v1

@clear
def test_message_send_success(helper):
    auth_user_id = helper.register_user(1)

    channel_id = helper.create_channel(1, auth_user_id)

    assert auth_user_id == 1
    assert channel_id == 1

    message_info = message_send_v1(auth_user_id, channel_id, "hello i hope this works")

    assert message_info.get('message_id') == 1

@clear
def test_message_length_over_1000(helper):
    auth_user_id = helper.register_user(1)

    channel_id = helper.create_channel(1, auth_user_id)

    assert auth_user_id == 1
    assert channel_id == 1

    msg = "e" * 1001

    with pytest.raises(InputError) as e: 
        message_send_v1(auth_user_id, channel_id, msg)
        assert "Message is more than 1000 characters" in str(e.value)

@clear
def test_message_length_1000(helper):
    auth_user_id = helper.register_user(1)

    channel_id = helper.create_channel(1, auth_user_id)

    assert auth_user_id == 1
    assert channel_id == 1

    msg = "e" * 100

    message_info = message_send_v1(auth_user_id, channel_id, msg)

    assert message_info.get('message_id') == 1


@clear
def test_message_user_not_in_channel(helper):
    auth_user_id = helper.register_user(1)

    intruder_id = helper.register_user(2)

    channel_id = helper.create_channel(1, auth_user_id)

    assert auth_user_id == 1
    assert channel_id == 1

    with pytest.raises(AccessError) as e: 
        message_send_v1(intruder_id, channel_id, "i hope this works")
        assert "Authorised user has not joined the channel" in str(e.value)

