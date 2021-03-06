import pytest
from src.channels import channels_list_v1,channels_create_v1
from src.error import InputError,AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from .helper import helper

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
    helper.register_users(9)
    helper.create_channels(2)
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']

    channels_create_v1(user_id, "correct", True)
    channels_create_v1(user_id, "correct2", True)
    channels_create_v1(user_id, "correct3", True)

    result = channels_list_v1(user_id)['channels']
    assert len(result) == 3

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
    assert channels_list_v1(user_id) == {}