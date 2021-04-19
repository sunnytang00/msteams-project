import pytest
import time
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_addowner_v1, channel_join_v1
from src.error import InputError, AccessError
from src.standup import standup_send_v1, standup_start_v1, standup_active_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_valid_input(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    length = 1
    time_finish = standup_start_v1(auth_user_id, ch_id, length).get('time_finish')
    standup_data = standup_active_v1(auth_user_id, ch_id)
    assert standup_data.get('is_active') == True and standup_data.get('time_finish') == time_finish

@clear
def test_no_standup_active(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    standup_data = standup_active_v1(auth_user_id, ch_id)
    assert standup_data.get('is_active') == False and standup_data.get('time_finish') == None

@clear
def test_invalid_channel(helper):
    auth_user_id = helper.register_user(1)
    ch_id = 10 
    with pytest.raises(InputError) as e: 
        standup_active_v1(auth_user_id, ch_id)
        assert f'Channel ID {ch_id} is not a valid channel' in str(e.value)

@clear
def test_invalid_token(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    with pytest.raises(AccessError) as e: 
        standup_active_v1(auth_user_id + 10, ch_id)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e.value)


