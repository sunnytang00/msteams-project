import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_details_v1
from tests.helper import clear

@clear
def test_valid_input():
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
    dm = dm_create_v1(auth_user_id, [user2_id])
    
    details = dm_details_v1(user2_id, dm['dm_id'])

    assert auth_user_id in [user['u_id'] for user in details['members']] and (
            user2_id in [user['u_id'] for user in details['members']])

@clear
def test_invalid_token():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm = dm_create_v1(auth_user_id, [])

    #make a invalid token
    u_id = auth_user_id + 10

    with pytest.raises(AccessError) as e:
        dm_details_v1(u_id, dm['dm_id'])
        assert f"token {u_id} does not refer to a valid user" in str(e.value)


@clear
def test_not_valid_dm():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #make a invalid dm_id
    dm_id = 10
    
    with pytest.raises(InputError) as e:
        dm_details_v1(auth_user_id, dm_id)
        assert f"dm_id {dm_id} does not refer to a valid dm" in str(e.value)

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
    dm = dm_create_v1(auth_user_id, [])

    with pytest.raises(AccessError) as e:
        dm_details_v1(user2_id, dm['dm_id'])
        assert f"auth_user {user2} is not member of dm {dm['dm_id']}" in str(e.value)
    