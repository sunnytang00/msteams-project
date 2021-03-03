import pytest
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1

def test_invaild_userID():
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channels_create_v1("invaild id here", "first channel" * 10, True)
        assert 'User ID is invaild' in str(e)

def test_vaild_input():
    clear_v1()
    user_id = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    channel_id = 1
    result = channels_create_v1(user_id['auth_user_id'], "correct", True)
    assert result == {'channel_id': channel_id} 

def test_name_length():
    clear_v1()
    user_id = auth_register_v1('bobsmith2@gmail.com','12345678','bob','smith')
    with pytest.raises(InputError) as e: 
        channels_create_v1(user_id['auth_user_id'], "first channel" * 10, True)
        assert 'Name is too long' in str(e)

def test_userID_not_exist():
    clear_v1()
    invalid_id = 10
    with pytest.raises(InputError) as e: 
        channels_create_v1(invalid_id, "second channel", True)
        assert f'User with id {invalid_id} does not exist' in str(e)

def test_duplicate_channel_name():
    clear_v1()
    user_id = auth_register_v1('bobsmith3@gmail.com','12345678','bob2','smith2')
    channel_name = "new channel2"
    channels_create_v1(user_id['auth_user_id'], channel_name, True)
    with pytest.raises(InputError) as e: 
        channels_create_v1(user_id['auth_user_id'], channel_name, True)
        assert f'Channel with name {channel_name} already exists' in str(e)
