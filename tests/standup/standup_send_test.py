import pytest
from src.base.channels import channels_create_v1
from src.base.channel import channel_details_v1, channel_addowner_v1, channel_join_v1
from src.base.error import InputError, AccessError
from src.base.standup import standup_send_v1
from src.base.other import clear_v1
from tests.helper import helper, clear

@clear 
def test_valid_input(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msgs = "1234"
    standup_send_v1(auth_user_id, ch_id, msgs)

@clear
def test_invalid_channel(helper):
    auth_user_id = helper.register_user(1)
    ch_id = 10 
    msg = "1234"
    with pytest.raises(InputError) as e: 
        standup_send_v1(auth_user_id, ch_id, msg)
        assert f'channel_id {ch_id} does not refer to a valid channel' in str(e.value)
@clear
def test_msg_too_long(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msg = "1234" * 1000
    with pytest.raises(InputError) as e: 
        standup_send_v1(auth_user_id, ch_id, msg)
        assert 'messages is too long' in str(e.value)
@clear
def test_invalid_token(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msg = "1234"
    with pytest.raises(AccessError) as e: 
        standup_send_v1(auth_user_id + 10, ch_id, msg)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e.value)
@clear
def test_not_member_of_channel(helper):
    auth_user_id = helper.register_user(1)
    user_id = helper.register_user(2)
    ch_id = helper.create_channel(2, user_id)
    msg = "1234"
    with pytest.raises(AccessError) as e: 
        standup_send_v1(auth_user_id, ch_id, msg)
        assert f'auth_user {auth_user_id} does not member of channel {ch_id}' in str(e.value)

'''
def test_standup_inactive(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msg = "1234"
    with pytest.raises(InputError) as e: 
        standup_send_v1(auth_user_id, ch_id, msg)
        assert f'messages is too long' in str(e.value)
'''
