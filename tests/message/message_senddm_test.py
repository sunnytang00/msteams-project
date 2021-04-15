import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_details_v1
from src.message import message_senddm_v1
from tests.helper import clear

@clear
def test_valid_input():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    msgs = "test"

    msg_id = message_senddm_v1(auth_user_id, dm_id, msgs).get('message_id')
    assert msg_id == 1

@clear
def test_msg_too_long():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    msgs = "test" * 1000

    with pytest.raises(InputError) as e:
        message_senddm_v1(auth_user_id, dm_id, msgs)
        assert "message is too long" in str(e.value)

@clear
def test_invalid_token():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    #make a invalid token
    u_id = auth_user_id + 10

    with pytest.raises(AccessError) as e:
        message_senddm_v1(u_id, dm_id, "test")
        assert f"token {u_id} does not refer to a valid user" in str(e.value)


@clear 
def test_auth_user_not_member():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    with pytest.raises(AccessError) as e:
        message_senddm_v1(user2_id, dm_id, "test")
        assert f"auth_user {user2} is not member of dm {dm_id}" in str(e.value)