import pytest
from src.base.channels import channels_create_v1
from src.base.error import InputError, AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from tests.helper import helper, clear

@clear
def test_invaild_userID():
    invalid_user_id = -1
    with pytest.raises(AccessError) as e: 
        channels_create_v1(invalid_user_id, "first channel" * 10, True)
        assert f'User ID {invalid_user_id} is invaild' in str(e)

    with pytest.raises(AccessError) as e: 
        channels_create_v1(2, "first channel" * 10, True)
        assert f'User ID {invalid_user_id} is invaild' in str(e)

@clear
def test_vaild_input():
    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']        
        
    channel_id = 1
    output = channels_create_v1(user_id, "correct", True)
    expected = {'channel_id': channel_id} 
    assert output == expected

@clear
def test_many_vaild_input(helper):
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

@clear
def test_name_length():
    user = auth_register_v1('bobsmith2@gmail.com','12345678','bob','smith')
    user_id = user['auth_user_id']

    invalid_name = "first channel" * 10
    with pytest.raises(InputError) as e: 
        channels_create_v1(user_id, invalid_name, True)
        assert f'Name {invalid_name} is more than 20 characters long' in str(e)

