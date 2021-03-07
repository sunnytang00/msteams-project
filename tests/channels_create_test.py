import pytest
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from .helper import helper

def test_invaild_userID():
    clear_v1()
    invalid_user_id = -1
    with pytest.raises(AccessError) as e: 
        channels_create_v1(invalid_user_id, "first channel" * 10, True)
        assert f'User ID {invalid_user_id} is invaild' in str(e)

    with pytest.raises(AccessError) as e: 
        channels_create_v1(2, "first channel" * 10, True)
        assert f'User ID {invalid_user_id} is invaild' in str(e)

def test_vaild_input():
    clear_v1()
    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']        
        
    channel_id = 1
    output = channels_create_v1(user_id, "correct", True)
    expected = {'channel_id': channel_id} 
    assert output == expected

def test_many_vaild_input(helper):
    clear_v1()
    helper.register_users(10)

    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']        
        

    channels_create_v1(user_id, "correct", True)
    channels_create_v1(user_id, "correct", True)
    channels_create_v1(user_id, "correct", True)
    channels_create_v1(user_id, "correct", True)
    output = channels_create_v1(user_id, "correct", True)

    channel_id = 5
    expected = {'channel_id': channel_id} 
    assert output == expected

def test_name_length():
    clear_v1()
    user = auth_register_v1('bobsmith2@gmail.com','12345678','bob','smith')
    user_id = user['auth_user_id']

    invalid_name = "first channel" * 10
    with pytest.raises(InputError) as e: 
        channels_create_v1(user_id, invalid_name, True)
        assert f'Name {invalid_name} is more than 20 characters long' in str(e)

