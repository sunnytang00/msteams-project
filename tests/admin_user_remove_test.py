import pytest
from src.base.channels import channels_create_v1
from src.base.channel import channel_details_v1, channel_addowner_v1
from src.base.admin import admin_userpermission_change_v1, admin_user_remove_v1
from src.base.error import InputError, AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from src.users.users import users_all_v1
from tests.helper import helper, clear

@clear
def test_valid_input():
    user1 = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user1['auth_user_id']
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user2['auth_user_id']

    admin_user_remove(user_id, u_id)

    assert u_id not in [k['u_id'] for user in users_all_v1()]

@clear
def test_invalid_token():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user['auth_user_id']

    #make a invalid auth_user_id
    user_id = u_id + 10

    with pytest.raises(AccessError) as e:
        admin_user_remove(user_id, u_id)
        assert f"token {user_id} does not refer to a valid token" in str(e)

@clear
def test_invalid_user():
    #register a user
    user1 = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user1['auth_user_id']

    #make a invalid u_id
    u_id = user_id + 10

    with pytest.raises(InputError) as e:
        admin_user_remove(user_id, u_id)
        assert f"user_id {u_id} does not refer to a valid user" in str(e)

@clear
def test_only_owner():
    #register a user
    user1 = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user1['auth_user_id']

    with pytest.raises(InputError) as e:
        admin_user_remove(user_id, user_id)
        assert f"user with user_id {user_id} is the only currently owner" in str(e)

@clear
def test_not_an_owner():
    #register users
    user1 = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user1['auth_user_id']
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user2['auth_user_id']

    with pytest.raises(AccessError) as e:
        admin_user_remove(u_id, user_id)
        assert f"user with user_id {u_id} is not owner of Dreams" in str(e)


