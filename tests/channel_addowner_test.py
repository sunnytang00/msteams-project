import pytest
from src.base.channels import channels_create_v1
from src.base.channel import channel_details_v1, channel_addowner_v1
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
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user_id2 = user2['auth_user_id']

    ch_name = "big fish"
    #create channel
    ch_id = channels_create_v1(user_id, ch_name, True)['channel_id']
    #add user2 as owner of channel
    channel_addowner_v1(user_id, chi_id, user_id2)

    #check the details of channel
    ch_details = channel_details_v1(user_id, ch_id)

    assert user_id2 in [user['u_id'] for user in ch_details['owner_members']]

def test_invalid_channel_id():
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

    #invaild id, there should be no channels exists
    ch_id = 3

    with pytest.raises(InputError) as e: 
        channel_addowner_v1(user_id, chi_id, user_id2)
        assert f'Channel ID {ch_id} is invaild' in str(e)

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

    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user_id2 = user2['auth_user_id']

    with pytest.raises(AccessError) as e: 
        channel_addowner_v1(user_id + 10, chi_id, user_id2)
        assert f'Token {user_id} is invaild' in str(e)

def test_is_already_owner_authorised():
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
        channel_addowner_v1(user_id, chi_id, user_id)
        assert f'Authorised user with ID {user_id} is arleady owner of channel' in str(e)

def test_is_already_owner():
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
    channel_addowner_v1(user_id, chi_id, user_id2)

    #add user2 as owner of channel again
    with pytest.raises(InputError) as e: 
        channel_addowner_v1(user_id, chi_id, user_id2)
        assert f' user with ID {user_id2} is arleady owner of channel' in str(e)
