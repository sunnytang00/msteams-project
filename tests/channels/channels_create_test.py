import pytest
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_invaild_userID():
    invalid_user_id = -1
    with pytest.raises(AccessError) as e: 
        channels_create_v1(invalid_user_id, "first channel" * 10, True)
        assert f'User ID {invalid_user_id} is invaild' in str(e.value)

    with pytest.raises(AccessError) as e: 
        channels_create_v1(2, "first channel" * 10, True)
        assert f'User ID {invalid_user_id} is invaild' in str(e.value)

@clear
def test_vaild_input(helper):
    auth_user_id = helper.register_user(1)
        
    channel_id = 1
    assert channels_create_v1(auth_user_id, "correct", True).get('channel_id') == channel_id

@clear
def test_many_vaild_input(helper):
    auth_user_id = helper.register_user(1)
    helper.create_channel(1, auth_user_id)
    helper.create_channel(2, auth_user_id)
    helper.create_channel(3, auth_user_id)
    helper.create_channel(4, auth_user_id)

    assert channels_create_v1(auth_user_id, "correct", True).get('channel_id') == 5

@clear
def test_name_length(helper):
    auth_user_id = helper.register_user(1)

    invalid_name = "first channel" * 10
    with pytest.raises(InputError) as e: 
        channels_create_v1(auth_user_id, invalid_name, True)
        assert f'Name {invalid_name} is more than 20 characters long' in str(e.value)

