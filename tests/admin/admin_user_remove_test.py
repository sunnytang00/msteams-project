import pytest
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_addowner_v1
from src.admin import admin_userpermission_change_v1, admin_user_remove_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.users import users_all_v1
from src.message import message_senddm_v1
from src.dm import dm_messages_v1, dm_create_v1, dm_details_v1
from tests.helper import helper, clear

@clear
def test_valid_input():
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

    admin_user_remove_v1(auth_user_id, u_id)

    assert u_id not in [user['u_id'] for user in users_all_v1(auth_user_id)]

@clear
def test_removed_user_dm_msg():
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

    #create a dm
    dm_id = dm_create_v1(auth_user_id, [u_id]).get('dm_id')

    #sent msg in dm
    message_senddm_v1(auth_user_id, dm_id, "user1 here")
    message_senddm_v1(u_id, dm_id, "user2 here")

    #remove user2
    admin_user_remove_v1(auth_user_id, u_id)

    messages = dm_messages_v1(auth_user_id, dm_id, 0)

    dms = dm_details_v1(auth_user_id, dm_id)

    assert messages['messages'][0]['message'] == 'Removed user' \
        and u_id not in [user['u_id'] for user in dms['members']]

@clear
def test_invalid_token():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user['auth_user_id']

    #make a invalid auth_user_id
    auth_user_id = u_id + 10

    with pytest.raises(AccessError) as e:
        admin_user_remove_v1(auth_user_id, u_id)
        assert f"token {auth_user_id} does not refer to a valid token" in str(e.value)

@clear
def test_invalid_user():
    #register a user
    user1 = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user1['auth_user_id']

    #make a invalid u_id
    u_id = auth_user_id + 10

    with pytest.raises(InputError) as e:
        admin_user_remove_v1(auth_user_id, u_id)
        assert f"auth_user_id {u_id} does not refer to a valid user" in str(e.value)

@clear
def test_only_owner():
    #register a user
    user1 = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user1['auth_user_id']

    with pytest.raises(InputError) as e:
        admin_user_remove_v1(auth_user_id, auth_user_id)
        assert f"user with auth_user_id {auth_user_id} is the only currently owner" in str(e.value)

@clear
def test_not_an_owner():
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

    with pytest.raises(AccessError) as e:
        admin_user_remove_v1(u_id, auth_user_id)
        assert f"user with auth_user_id {u_id} is not owner of Dreams" in str(e.value)

@clear
def test_remove_only_member_of_channel():
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

    #create a channel
    ch_id = channels_create_v1(u_id, "no member soon", True).get('channel_id')
    
    #remove user2
    admin_user_remove_v1(auth_user_id, u_id)

    #make user1 as owner of channel
    channel_addowner_v1(auth_user_id, ch_id, auth_user_id)

    #check details of channel
    channel = channel_details_v1(auth_user_id, ch_id)

    #check if the user2 being removed from channel's member
    assert u_id not in [user['u_id'] for user in channel['owner_members']] and (
            u_id not in [user['u_id'] for user in channel['all_members']])

@clear
def test_remove_Dream_owner(helper):
    auth_user_id = helper.register_user(1)
    u_id = helper.register_user(2)

    admin_userpermission_change_v1(auth_user_id, u_id, permission_id = 1)

    admin_user_remove_v1(auth_user_id, u_id)

    assert u_id not in [user['u_id'] for user in users_all_v1(auth_user_id)]

