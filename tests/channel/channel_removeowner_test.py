import pytest
from src.base.channels import channels_create_v1
from src.base.channel import channel_details_v1, channel_addowner_v1, channel_removeowner_v1
from src.base.error import InputError, AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from tests.helper import helper, clear

@clear
def test_valid_input():
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
    channel_removeowner_v1(user_id, ch_id, user_id2)
    #check the details of channel
    ch_details = channel_details_v1(user_id, ch_id)

    assert user_id2 not in [user['u_id'] for user in ch_details['owner_members']]

@clear
def test_invalid_channel_id():
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
        channel_removeowner_v1(user_id, ch_id, user_id2)
        assert f'channel_id {ch_id} does not refer to a valid channel' in str(e)

@clear
def test_invalid_token():
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
        channel_removeowner_v1(user_id + 10, ch_id, user_id2)
        assert f'token {user_id} does not refer to a valid token' in str(e)

@clear
def test_the_only_owner():
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    ch_name = "big fish"

    ch_id = channels_create_v1(user_id, ch_name, True)['channel_id']

    with pytest.raises(InputError) as e: 
        channel_removeowner_v1(user_id, ch_id, user_id)
        assert f'user with {user_id} is the only owner of channel' in str(e)

@clear
def test_user_is_not_owner():
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
        channel_removeowner_v1(user_id, ch_id, user_id2)
        assert f'user with {user_id} is not owner of channel' in str(e)

@clear
def test_auth_user_has_no_access():
    #register the owner of Dreams
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']
    #register 
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user_id2 = user2['auth_user_id']

    user3 = auth_register_v1(email='harrypotter20@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user_id3 = user3['auth_user_id']

    ch_name = "big fish"

    ch_id = channels_create_v1(user_id2, ch_name, True)['channel_id']

    channel_addowner_v1(user_id2, ch_id, user_id)

    with pytest.raises(AccessError) as e: 
        channel_removeowner_v1(user_id3, ch_id, user_id)
        assert f'Auth_user with id {user_id} is not owner of channel or owner of dreams' in str(e)


@clear
def test_auth_user_is_owner_of_Dream():
    #register the owner of Dreams
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']
    #register 
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user_id2 = user2['auth_user_id']

    user3 = auth_register_v1(email='harrypotter20@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user_id3 = user3['auth_user_id']

    ch_name = "big fish"

    ch_id = channels_create_v1(user_id2, ch_name, True)['channel_id']

    channel_addowner_v1(user_id, ch_id, user_id3)
    channel_removeowner_v1(user_id, ch_id, user_id2)
        #check the details of channel
    ch_details = channel_details_v1(user_id2, ch_id)

    assert (user_id3 in [user['u_id'] for user in ch_details['owner_members']]) and (
            user_id2 not in [user['u_id'] for user in ch_details['owner_members']])

'''
more test needed when add permission functions finished
'''