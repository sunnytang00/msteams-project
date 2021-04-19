import pytest
from src.channels import channels_listall_v1,channels_create_v1
from src.error import InputError,AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_invaild_userID():
    with pytest.raises(AccessError) as e: 
        channels_listall_v1(-2)
        assert 'User ID is invaild' in str(e.value)

@clear
def test_vaild_input(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)

    channels_create_v1(auth_user_id, "correct", True)
    channels_create_v1(auth_user_id_2, "correct4", True)
    channels_create_v1(auth_user_id_2, "correct5", True)

    assert len(channels_listall_v1(auth_user_id_2)['channels']) == 3

@clear
def test_private_channel_exists(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)

    ch1 = channels_create_v1(auth_user_id_2, "correct", False)['channel_id']
    ch2 = channels_create_v1(auth_user_id, "correct2", True)['channel_id']

    expected1 = {'channel_id' : ch1, 'name' : 'correct'}
    expected2 = {'channel_id' : ch2, 'name' : 'correct2'}
    ch_lst = channels_listall_v1(auth_user_id)['channels']
    assert (expected1 not in ch_lst) and (expected2  in ch_lst)

@clear
def test_check_content(helper):
    auth_user_id = helper.register_user(1)

    ch = channels_create_v1(auth_user_id, "correct", True)['channel_id']

    expected = {'channel_id' : ch, 'name': 'correct'}

    assert  expected in channels_listall_v1(auth_user_id)['channels']