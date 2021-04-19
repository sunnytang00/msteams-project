import pytest
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_valid_input():
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    channel = channels_create_v1(auth_user_id, 'Cat Society', True)
    channel_id = channel['channel_id']

    output = channel_details_v1(auth_user_id=auth_user_id, channel_id=channel_id)

    assert auth_user_id in [users['u_id'] for users in output['all_members']]

@clear
def test_invalid_token(helper):
    auth_user_id = 10

    u_id = helper.register_user(1)

    ch_id = channels_create_v1(u_id, "big fish", True)['channel_id']
    with pytest.raises(AccessError) as e: 
        channel_details_v1(auth_user_id=auth_user_id, channel_id=ch_id)
        assert f'u_id {auth_user_id} does not refer to a valid user' in str(e.value)

@clear
def test_invalid_channel_id():
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    invalid_channel_id = 9

    with pytest.raises(InputError) as e: 
        channel_details_v1(auth_user_id=auth_user_id, channel_id=invalid_channel_id)
        assert f'Channel ID {invalid_channel_id} is not a valid channel.' in str(e.value)

@clear
def test_user_not_authorised():
    """Authorised user is not a member of channel with channel_id"""
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    channel_owner_user = auth_register_v1(email='harrypotter7@gmail.com',
                                            password='qw3rtyAppl3s@99',
                                            name_first='Harry',
                                            name_last='Potter')
    channel_owner_user_id = channel_owner_user['auth_user_id']    

    channel = channels_create_v1(channel_owner_user_id, 'Cat Society', True)
    channel_id = channel['channel_id']

    with pytest.raises(AccessError) as e: 
        channel_details_v1(auth_user_id=auth_user_id, channel_id=channel_id)
        assert f'Authorised user {auth_user_id} is not a member of channel with channel_id {channel_id}' in str(e.value)
