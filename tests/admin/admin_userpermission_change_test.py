import pytest
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_addowner_v1
from src.admin import admin_userpermission_change_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_valid_input():
    #register users
    user1 = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user1['auth_user_id']
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user2['auth_user_id']

    #change permission of user2 as owner
    admin_userpermission_change_v1(auth_user_id, u_id, permission_id = 1)

    #create a channel with user1
    ch_id = channels_create_v1(auth_user_id, 'owner', True)['channel_id']

    # user2 added himself as owner of channel
    channel_addowner_v1(u_id, ch_id, u_id)
    #check if user2 becomes the owner of channel
    channel = channel_details_v1(u_id, ch_id)
    assert u_id in [user['u_id'] for user in channel['owner_members']]

@clear
def test_invalid_token():
    #register a user
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    u_id = user['auth_user_id']

    #make a invalid token_id
    auth_user_id = u_id + 10
    with pytest.raises(AccessError) as e:
        admin_userpermission_change_v1(auth_user_id, u_id, permission_id = 2)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e.value)

@clear
def test_invalid_user():

    #register a user
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    #make a invalid id
    u_id = auth_user_id + 10
    with pytest.raises(InputError) as e:
        admin_userpermission_change_v1(auth_user_id, u_id, permission_id = 2)
        assert f'u_id {u_id} does not refer to a valid user id' in str(e.value)

@clear
def test_invalid_permission_id():
    #register users
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user2['auth_user_id']

    permission_id = 4
    with pytest.raises(InputError) as e:
        admin_userpermission_change_v1(auth_user_id, u_id, permission_id)
        assert f'permission_id {permission_id} does not refer to a valid permisison id' in str(e.value)

@clear
def test_not_owner():
    #register users
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user2['auth_user_id']

    with pytest.raises(AccessError) as e:
        admin_userpermission_change_v1(u_id, auth_user_id, permission_id = 2)
        assert f'user id {u_id} is not owner of Dreams' in str(e.value)

