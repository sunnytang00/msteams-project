import pytest
from src.base.channels import channels_create_v1
from src.base.channel import channel_details_v1, channel_addowner_v1, channel_join_v1
from src.base.error import InputError, AccessError
from src.base.standup import standup_send_v1, startup_start_v1
from src.base.other import clear_v1
from tests.helper import helper, clear
'''
def test_valid_input():

'''
def test_invalid_channel():
    auth_user_id = helper.register_user(1)
    ch_id = 10 
    length = 10
    with pytest.raises(InputError) as e: 
        standup_start_v1(auth_user_id, ch_id, length)
        assert f'Channel ID {ch_id} is not a valid channel' in str(e.value)

def test_standup_already_started():
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    length = 10
    standup_start_v1(auth_user_id, ch_id, length)
    with pytest.raises(InputError) as e: 
        standup_start_v1(auth_user_id, ch_id, length)
        assert 'An active standup is currently running in this channel' in str(e.value)

def test_invalid_token():
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    length = 10
    with pytest.raises(AccessError) as e: 
        standup_start_v1(auth_user_id + 10, ch_id, length)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e.value)

def test_not_member_in_channel():
    auth_user_id = helper.register_user(1)
    user_id = helper.register_user(2)
    ch_id = helper.create_channel(2, user_id)
    length = 10
    with pytest.raises(AccessError) as e: 
        standup_start_v1(auth_user_id, ch_id, length)
        assert 'Authorised user is not in the channel' in str(e.value)



