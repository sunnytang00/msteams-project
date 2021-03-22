import pytest
from src.base.channels import channels_create_v1
from src.base.channel import channel_details_v1, channel_addowner_v1, channel_removeowner_v1, channel_leave_v1
from src.base.error import InputError, AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from tests.helper import helper

def test_valid_input():
    clear_v1()
    #register
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    ch_name = "big fish"
    #create channel
    ch_id = channels_create_v1(user_id, ch_name, True)['channel_id']
    #add user2 as owner of channel
    channel_leave_v1(user_id, ch_id)
    #check the details of channel
    ch_details = channel_details_v1(user_id, ch_id)

    assert user_id not in [user['u_id'] for user in ch_details['owner_members']] and (
            user_id not in [user['u_id'] for user in ch_details['all_members']]
    )

def test_multiple_users():
    clear_v1()
    #register
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user_id2 = user2['auth_user_id']

    ch_name = "big fish"
    #create channel
    ch_id = channels_create_v1(user_id, ch_name, True)['channel_id']
    #add user2 as owner of channel
    channel_addowner_v1(user_id, ch_id, user_id2)
    #user2 leaves channel
    channel_leave_v1(user_id2, ch_id)
    #check the details of channel
    ch_details = channel_details_v1(user_id, ch_id)

    assert user_id2 not in [user['u_id'] for user in ch_details['owner_members']] and (
            user_id2 not in [user['u_id'] for user in ch_details['all_members']]
    )

def test_invalid_channel_id():
    clear_v1()
    #register
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    #invaild id, there should be no channels exists
    ch_id = 3

    with pytest.raises(InputError) as e: 
        channel_leave_v1(user_id, ch_id)
        assert f'channel_id {ch_id} does not refer to a valid channel' in str(e)

def test_invalid_token():
    clear_v1()
    #register
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    ch_name = "big fish"

    ch_id = channels_create_v1(user_id, ch_name, True)['channel_id']
    with pytest.raises(AccessError) as e: 
        channel_leave_v1(user_id + 10, ch_id)
        assert f'token {user_id} does not refer to a valid token' in str(e)


def test_user_is_not_member():
    clear_v1()
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user_id2 = user2['auth_user_id']

    ch_name = "big fish"

    ch_id = channels_create_v1(user_id, ch_name, True)['channel_id']

    with pytest.raises(InputError) as e: 
        channel_leave_v1(user_id2, ch_id)
        assert f'user with {user_id} is not member of channel' in str(e)


