import pytest
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_addowner_v1, channel_join_v1
from src.error import InputError, AccessError
from src.standup import standup_send_v1, standup_start_v1
from src.other import clear_v1
from tests.helper import helper, clear

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

@clear
def test_standup_inactive(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msg = "1234"
    
    with pytest.raises(InputError) as e: 
        standup_send_v1(auth_user_id, ch_id, msg)
        assert f'An active standup is not currently running in this channel' in str(e.value)
