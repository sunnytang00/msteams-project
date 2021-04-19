import pytest
from src.channel import channel_join_v1
from src.channels import channels_list_v1,channels_create_v1
from src.error import InputError,AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_invaild_userID(helper):
    with pytest.raises(AccessError) as e: 
        channels_list_v1(-1)
        assert 'User ID is invaild' in str(e.value)

    with pytest.raises(AccessError) as e: 
        channels_list_v1(8)
        assert 'User ID is invaild' in str(e.value)

@clear
def test_vaild_input(helper):
    auth_user_id = helper.register_user(1)

    ch1 = channels_create_v1(auth_user_id, "correct", True)['channel_id']
    ch2 = channels_create_v1(auth_user_id, "correct2", True)['channel_id']
    ch3 = channels_create_v1(auth_user_id, "correct3", False)['channel_id']
    expected = [{'channel_id' : ch1, 'name' : 'correct'},
                {'channel_id' : ch2, 'name' : 'correct2'},
                {'channel_id' : ch3, 'name' : 'correct3'}]
    expected = sorted(expected, key=lambda ch: ch['channel_id'])


    result = channels_list_v1(auth_user_id)['channels']
    result = sorted(result, key=lambda ch: ch['channel_id'])
    assert expected == result

@clear
def test_multiple_user_exists(helper):
    auth_user_id = helper.register_user(1)
    helper.create_channel(1, auth_user_id)
    helper.create_channel(2, auth_user_id)

    auth_user_id_2 = helper.register_user(2)

    result = channels_list_v1(auth_user_id_2).get('channels')
    assert len(result) == 0

@clear
def test_no_channel_exists(helper):
    auth_user_id = helper.register_user(1)
    assert channels_list_v1(auth_user_id)['channels'] == []

@clear
def test_member_of_channels_private(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)

    ch_id = channels_create_v1(auth_user_id, "correct", True)['channel_id']

    channel_join_v1(auth_user_id_2, ch_id)
    expected = {'channel_id' : ch_id, 'name' : 'correct'}
    assert expected in channels_list_v1(auth_user_id_2)['channels']
