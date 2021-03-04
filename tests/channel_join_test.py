import pytest
from src.channel import channel_join_v1
from src.channels import channels_create_v1, channels_list_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import Helper

def test_invalid_userID():
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channel_join_v1("invaild id here", 0)
        assert 'User ID is invalid' in str(e)

def test_valid_input():
    clear_v1()
    user_id = auth_register_v1(email='bobsmith1@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')

    user_id2 = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob2',
                                name_last='smith2')
    channel_id = channels_create_v1(user_id['auth_user_id'], "channel1", True)
    channel_join_v1(user_id2['auth_user_id'], channel_id['channel_id'])
    result = channels_list_v1(user_id2['auth_user_id'])
    assert len(result) == 1

def test_invalid_channelID():
    clear_v1()
    Helper.register_users(1)
    Helper.create_channels(1)
    invalid_id = 10
    with pytest.raises(InputError) as e: 
        channel_join_v1(1, invalid_id)
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

def test_channel_not_exist():
    clear_v1()
    Helper.register_users(1)
    channel_id = 1
    with pytest.raises(InputError) as e: 
        channel_join_v1(1, channel_id)
        assert 'Channel with ID {channel_id} does not exist' in str(e)

def test_already_member_of_channel():
    clear_v1()
    user_id = auth_register_v1(email='bobsmith1@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_id2 = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob2',
                                name_last='smith2')
                                
    channel_id = channels_create_v1(user_id['auth_user_id'], "channel1", True)
    channel_join_v1(user_id2['auth_user_id'], channel_id['channel_id'])
    with pytest.raises(InputError) as e: 
        channel_join_v1(user_id2['auth_user_id'], channel_id['channel_id'])
        assert 'The user is already in the channel' in str(e)

    