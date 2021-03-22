import pytest
from src.base.channels import channels_listall_v1,channels_create_v1
from src.base.error import InputError,AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from tests.helper import helper

def test_invaild_userID():
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channels_listall_v1(-2)
        assert 'User ID is invaild' in str(e)

def test_vaild_input(helper):
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
    user_2_id = user_2['auth_user_id']

    channels_create_v1(user_id, "correct", True)
    channels_create_v1(user_2_id, "correct4", True)
    channels_create_v1(user_2_id, "correct5", True)

    assert len(channels_listall_v1(user_2_id)['channels']) == 3

def test_private_channel_exists(helper):
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
    user_2_id = user_2['auth_user_id']

    ch1 = channels_create_v1(user_2_id, "correct", False)['channel_id']
    ch2 = channels_create_v1(user_id, "correct2", True)['channel_id']
    expected1 = {'channel_id' : ch1, 'name' : 'correct'}
    expected2 = {'channel_id' : ch2, 'name' : 'correct2'}
    ch_lst = channels_listall_v1(user_id)['channels']
    assert (expected1 not in ch_lst) and (expected2  in ch_lst)

def test_check_content(helper):
    clear_v1()
    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']


    ch = channels_create_v1(user_id, "correct", True)['channel_id']

    expected = {'channel_id' : ch, 'name': 'correct'}

    assert  expected in channels_listall_v1(user_id)['channels']