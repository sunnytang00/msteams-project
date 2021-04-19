import pytest
from src.channel import channel_invite_v1
from src.channels import channels_create_v1, channels_listall_v1 ,channels_list_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_valid_input(helper):
    invitor_user_id = helper.register_user(1)
    invitee_user_id = helper.register_user(2)

    channel = channels_create_v1(invitor_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    channel_invite_v1(auth_user_id=invitor_user_id, channel_id=channel_id, u_id=invitee_user_id)

    channels = channels_listall_v1(2)
    output = channels['channels'][0]['channel_id']
    expected = 1
    assert output == expected

@clear
def test_invalid_channel_id(helper):
    invitor_user_id = helper.register_user(1)
    invitee_user_id = helper.register_user(2)

    invalid_channel_id = 4 
    with pytest.raises(InputError) as e: 
        channel_invite_v1(auth_user_id=invitor_user_id, channel_id=invalid_channel_id, u_id=invitee_user_id)
        assert f'Channel ID {invalid_channel_id} does not exist.' in str(e.value)

@clear
def test_invalid_token(helper):
    invitor_user_id = 10
    invitee_user_id = helper.register_user(2)

    ch_id = channels_create_v1(invitee_user_id, "big fish", True)['channel_id']
    with pytest.raises(AccessError) as e: 
        channel_invite_v1(auth_user_id=invitor_user_id, channel_id=ch_id, u_id=invitee_user_id)
        assert f'u_id {invitor_user_id} does not refer to a valid user' in str(e.value)

@clear
def test_invalid_u_id(helper):
    invitor_user_id = helper.register_user(1)
    invitee_user_id = 10

    ch_id = channels_create_v1(invitor_user_id, "big fish", True)['channel_id']
    with pytest.raises(InputError) as e: 
        channel_invite_v1(auth_user_id=invitor_user_id, channel_id=ch_id, u_id=invitee_user_id)
        assert f'u_id {invitee_user_id} does not refer to a valid user' in str(e.value)
'''
@clear
def test_invaild_userID(helper):
    invalid_user_id = -1
    with pytest.raises(AccessError) as e: 
        channels_create_v1(invalid_user_id, "first", True)
        assert f'User ID {invalid_user_id} is invaild' in str(e.value)

    clear_v1()
    invalid_user_id = 2
    with pytest.raises(AccessError) as e: 
        channels_create_v1(invalid_user_id, "first", True)
        assert f'User ID {invalid_user_id} is invaild' in str(e.value)
'''
@clear
def test_vaild_input(helper):
    auth_user_id = helper.register_user(1)
        
    channel_id = 1
    output = channels_create_v1(auth_user_id, "correct", True)
    expected = {'channel_id': channel_id} 
    assert output == expected

@clear
def test_name_length(helper):
    auth_user_id = helper.register_user(1)

    invalid_name = "first channel" * 10
    with pytest.raises(InputError) as e: 
        channels_create_v1(auth_user_id, invalid_name, True)
        assert f'Name {invalid_name} is more than 20 characters long' in str(e.value)


    """the authorised user is not already a member of the channel"""
    clear_v1()
    invitor_user_id = helper.register_user(1)
    invitee_user_id = helper.register_user(2)
    channel_owner_user_id = helper.register_user(3)

    channel = channels_create_v1(channel_owner_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    with pytest.raises(AccessError) as e: 
        channel_invite_v1(auth_user_id=invitor_user_id, channel_id=channel_id, u_id=invitee_user_id)
        assert f'the authorised user {invitor_user_id} is not already a member of the channel' in str(e.value)