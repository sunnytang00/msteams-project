import pytest
from src.channels import channels_listall_v1,channels_create_v1
from src.data import data
from src.error import InputError,AccessError
from src.auth import auth_register_v1
from src.other import clear_v1

def test_invaild_userID():
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channels_listall_v1("invaild id here")
        assert 'User ID is invaild' in str(e)

def test_vaild_input():
    clear_v1()
    user_id = auth_register_v1('bobsmith2@gmail.com','12345678','bob','smith')
    channels_create_v1(user_id['auth_user_id'], "correct", True)
    channels_create_v1(user_id['auth_user_id'], "correct2", True)
    channels_create_v1(user_id['auth_user_id'], "correct3", True)
    assert len(channels_listall_v1(user_id['auth_user_id'])) == 3

 
