import pytest
from src.channels import channels_listall_v1,channels_create_v1
from src.error import InputError,AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
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

    assert len(channels_listall_v1(user_2_id)) == 3

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

    channels_create_v1(user_id, "correct", False)
    channels_create_v1(user_id, "correct2", False)
    channels_create_v1(user_id, "correct3", False)
    channels_create_v1(user_2_id, "correct4", True)
    channels_create_v1(user_2_id, "correct5", True)

    assert len(channels_listall_v1(user_2_id)) == 2