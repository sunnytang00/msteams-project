import pytest
from src.channel import channel_invite_v1
from src.channels import channels_create_v1, channels_listall_v1 ,channels_list_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper

def test_valid_input():
    clear_v1()
    invitor_user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    invitor_user_id = invitor_user['auth_user_id']

    invitee_user = auth_register_v1(email='batman777@gmail.com',
                                password='12as548',
                                name_first='Bat',
                                name_last='Man')
    invitee_user_id = invitee_user['auth_user_id']

    channel = channels_create_v1(invitor_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    channel_invite_v1(auth_user_id=invitor_user_id, channel_id=channel_id, u_id=invitee_user_id)

    channels = channels_listall_v1(2)
    output = channels[0]['channel_id']
    expected = 1
    assert output == expected

def test_invalid_channel_id():
    clear_v1()
    invitor_user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    invitor_user_id = invitor_user['auth_user_id']

    invitee_user = auth_register_v1(email='batman777@gmail.com',
                                password='12as548',
                                name_first='Bat',
                                name_last='Man')
    invitee_user_id = invitee_user['auth_user_id']

    invalid_channel_id = 4 
    with pytest.raises(InputError) as e: 
        channel_invite_v1(auth_user_id=invitor_user_id, channel_id=invalid_channel_id, u_id=invitee_user_id)
        assert f'Channel ID {invalid_channel_id} does not exist.' in str(e)


import pytest
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1

def test_invaild_userID():
    clear_v1()
    invalid_user_id = -1
    with pytest.raises(AccessError) as e: 
        channels_create_v1(invalid_user_id, "first", True)
        assert f'User ID {invalid_user_id} is invaild' in str(e)

    clear_v1()
    invalid_user_id = 2
    with pytest.raises(AccessError) as e: 
        channels_create_v1(invalid_user_id, "first", True)
        assert f'User ID {invalid_user_id} is invaild' in str(e)

def test_vaild_input():
    clear_v1()
    user = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id = user['auth_user_id']        
        
    channel_id = 1
    output = channels_create_v1(user_id, "correct", True)
    expected = {'channel_id': channel_id} 
    assert output == expected

def test_name_length():
    clear_v1()
    user = auth_register_v1('bobsmith2@gmail.com','12345678','bob','smith')
    user_id = user['auth_user_id']

    invalid_name = "first channel" * 10
    with pytest.raises(InputError) as e: 
        channels_create_v1(user_id, invalid_name, True)
        assert f'Name {invalid_name} is more than 20 characters long' in str(e)


    """the authorised user is not already a member of the channel"""
    clear_v1()
    invitor_user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    invitor_user_id = invitor_user['auth_user_id']

    invitee_user = auth_register_v1(email='batman777@gmail.com',
                                password='12a548',
                                name_first='Bat',
                                name_last='Man')
    invitee_user_id = invitee_user['auth_user_id']

    channel_owner_user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    channel_owner_user_id = channel_owner_user['auth_user_id']            

    channel = channels_create_v1(channel_owner_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    with pytest.raises(AccessError) as e: 
        channel_invite_v1(auth_user_id=invitor_user_id, channel_id=channel_id, u_id=invitee_user_id)
        assert f'the authorised user {invitor_user_id} is not already a member of the channel' in str(e)