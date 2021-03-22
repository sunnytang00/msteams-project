import pytest
from src.base.channel import channel_join_v1
from src.base.channels import channels_list_v1,channels_create_v1
from src.base.error import InputError,AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from tests.helper import helper

def test_invaild_userID(helper):
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channels_list_v1(-1)
        assert 'User ID is invaild' in str(e)

    with pytest.raises(AccessError) as e: 
        channels_list_v1(8)
        assert 'User ID is invaild' in str(e)

def test_vaild_input(helper):
    clear_v1()
   # helper.register_users(9)
   # helper.create_channels(2)
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']

    ch1 = channels_create_v1(user_id, "correct", True)['channel_id']
    ch2 = channels_create_v1(user_id, "correct2", True)['channel_id']
    ch3 = channels_create_v1(user_id, "correct3", False)['channel_id']
    expected = [{'channel_id' : ch1, 'name' : 'correct'},
                {'channel_id' : ch2, 'name' : 'correct2'},
                {'channel_id' : ch3, 'name' : 'correct3'}]
    expected = sorted(expected, key=lambda ch: ch['channel_id'])

    result = channels_list_v1(user_id)['channels']
    result = sorted(result, key=lambda ch: ch['channel_id'])
    assert expected == result

def test_multiple_user_exists(helper):
    clear_v1()
    helper.register_users(5)
    helper.create_channels(5)
    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']
    channels_create_v1(user_id, "correct4", True)
    channels_create_v1(user_id, "correct5", True)

    user_2 = auth_register_v1(email='janetsmith4@gmail.com',
                                password='12345678',
                                name_first='Janet',
                                name_last='Smith')
    user_id_2 = user_2['auth_user_id']
    result = channels_list_v1(user_id_2)['channels']
    assert len(result) == 0

def test_no_channel_exists(helper):
    clear_v1()
    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']
    assert channels_list_v1(user_id)['channels'] == []

def test_member_of_channels_private(helper):
    clear_v1()
    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']

    user_2 = auth_register_v1(email='janetsmith4@gmail.com',
                                password='12345678',
                                name_first='Janet',
                                name_last='Smith')
    user_id_2 = user_2['auth_user_id']

    ch_id = channels_create_v1(user_id, "correct", True)['channel_id']
    channel_join_v1(user_id_2, ch_id)
    expected = {'channel_id' : ch_id, 'name' : 'correct'}
    print(channels_list_v1(user_id))
    assert expected in channels_list_v1(user_id_2)['channels']