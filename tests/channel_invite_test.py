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
                                name_first='bob',
                                name_last='smith')
    invitor_user_id = invitor_user['auth_user_id']

    invitee_user = auth_register_v1(email='batman777@gmail.com',
                                password='12as548',
                                name_first='bat',
                                name_last='man')
    invitee_user_id = invitee_user['auth_user_id']

    channel = channels_create_v1(invitor_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    channel_invite_v1(auth_user_id=invitor_user_id, channel_id=channel_id, u_id=invitee_user_id)

    channels = channels_listall_v1(2)
    assert channels[-1]['id'] == 1

def test_invalid_channel_id():
    clear_v1()
    invitor_user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='bob',
                                name_last='smith')
    invitor_user_id = invitor_user['auth_user_id']

    invitee_user = auth_register_v1(email='batman777@gmail.com',
                                password='12as548',
                                name_first='bat',
                                name_last='man')
    invitee_user_id = invitee_user['auth_user_id']

    invalid_channel_id = 4 
    with pytest.raises(InputError) as e: 
        channel_invite_v1(auth_user_id=invitor_user_id, channel_id=invalid_channel_id, u_id=invitee_user_id)
        assert 'Channel id does not exist.' in str(e)


def test_invalid_auth_user_id():
    clear_v1()
    invalid_invitor_user_id = 5

    invitee_user = auth_register_v1(email='batman777@gmail.com',
                                password='12as548',
                                name_first='bat',
                                name_last='man')
    invitee_user_id = invitee_user['auth_user_id']

    # TODO: change harded value from 1
    channel = channels_create_v1(1, "Cat Society", True)
    channel_id = channel['channel_id']
    with pytest.raises(InputError) as e: 
        channel_invite_v1(auth_user_id=invalid_invitor_user_id, channel_id=channel_id, u_id=invitee_user_id)
        assert 'User ID does not refer to a valid user.' in str(e)

def test_invalid_u_id():
    clear_v1()
    invitor_user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='bob',
                                name_last='smith')
    invitor_user_id = invitor_user['auth_user_id']

    invalid_invitee_user_id = 14 

    channel = channels_create_v1(invitor_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    with pytest.raises(InputError) as e: 
        channel_invite_v1(auth_user_id=invitor_user_id, channel_id=channel_id, u_id=invalid_invitee_user_id)
        assert 'User ID does not refer to a valid user.' in str(e)

# TODO: AccessError expection test