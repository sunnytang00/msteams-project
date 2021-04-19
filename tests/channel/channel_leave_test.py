import pytest
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_addowner_v1, channel_removeowner_v1, channel_leave_v1, channel_join_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_multiple_users(helper):
    #register
    auth_user_id = helper.register_user(1)
    u_id2 = helper.register_user(2)
    u_id3 = helper.register_user(3)
    ch_name = "big fish"
    #create channel
    ch_id = channels_create_v1(auth_user_id, ch_name, True)['channel_id']
    #add user2 as owner of channel
    channel_addowner_v1(auth_user_id, ch_id, u_id2)
    channel_join_v1(u_id3, ch_id)
    #user2 leaves channel
    channel_leave_v1(u_id2, ch_id)
    channel_leave_v1(u_id3, ch_id)
    #check the details of channel
    ch_details = channel_details_v1(auth_user_id, ch_id)

    assert u_id2 not in [user['u_id'] for user in ch_details['owner_members']] and \
            u_id2 not in [user['u_id'] for user in ch_details['all_members']] and \
            u_id3 not in [user['u_id'] for user in ch_details['owner_members']] and \
            u_id3 not in [user['u_id'] for user in ch_details['all_members']]

@clear
def test_invalid_channel_id():
    #register
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    #invaild id, there should be no channels exists
    ch_id = 3

    with pytest.raises(InputError) as e: 
        channel_leave_v1(auth_user_id, ch_id)
        assert f'channel_id {ch_id} does not refer to a valid channel' in str(e.value)

@clear
def test_invalid_token():
    #register
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    ch_name = "big fish"

    ch_id = channels_create_v1(auth_user_id, ch_name, True)['channel_id']
    with pytest.raises(AccessError) as e: 
        channel_leave_v1(auth_user_id + 10, ch_id)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e.value)


@clear
def test_user_is_not_member():
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    auth_user_id_2 = user2['auth_user_id']

    ch_name = "big fish"

    ch_id = channels_create_v1(auth_user_id, ch_name, True)['channel_id']

    with pytest.raises(AccessError) as e: 
        channel_leave_v1(auth_user_id_2, ch_id)
        assert f'user with {auth_user_id} is not member of channel' in str(e.value)
