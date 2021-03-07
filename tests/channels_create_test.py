import pytest
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1

def test_invaild_userID():
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channels_create_v1(-1, "first channel" * 10, True)
        assert 'User ID is invaild' in str(e)

    with pytest.raises(AccessError) as e: 
        channels_create_v1(2, "first channel" * 10, True)
        assert 'User ID is invaild' in str(e)

def test_vaild_input():
    clear_v1()
    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']        
        
    channel_id = 1
    result = channels_create_v1(user_id, "correct", True)
    assert result == {'channel_id': channel_id} 

def test_name_length():
    clear_v1()
    user = auth_register_v1('bobsmith2@gmail.com','12345678','bob','smith')
    user_id = user['auth_user_id']

    with pytest.raises(InputError) as e: 
        channels_create_v1(user_id, "first channel" * 10, True)
        assert 'Name is more than 20 characters long' in str(e)

