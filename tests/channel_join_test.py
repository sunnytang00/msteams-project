import pytest
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from helper import register_users, create_channels

def test_invalid_userID():
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channel_join_v1("invaild id here", 0)
        assert 'User ID is invalid' in str(e)

def test_invalid_ChannelID():
    clear_v1()
    register_users(1)
    create_channels(1)
    invalid_id = 10
    with pytest.raises(InputError) as e: 
        channel_join_v1(user_id['auth_user_id'], invaild_id)
        assert 'Channel ID is invalid' in str(e)

def test_access_to_private():
    clear_v1()
    user_id = auth_register_v1(email='bobsmith1@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')

    user_id2 = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob2',
                                name_last='smith2')

    channel_id1 = channels_create_v1(user_id['auth_user_id'], "channel1", False)
    channel_id2 = channels_create_v1(user_id['auth_user_id'], "channel2", False)
    with pytest.raises(AccessError) as e: 
        channel_join_v1(user_id['auth_user_id'], channel_id2['channel_id'])
        assert 'Cannot access the private channel' in str(e)

