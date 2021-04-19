import pytest
from src.channel import channel_join_v1
from src.channels import channels_create_v1, channels_list_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_valid_input():
    user = auth_register_v1(email='bobsmith1@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith'
                            )
    auth_user_id = user['auth_user_id']

    user_2 = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12as548',
                                name_first='bob2',
                                name_last='smith2')
    user_id_2 = user_2['auth_user_id']

    channel = channels_create_v1(auth_user_id, "channel1", True)
    channel_join_v1(user_id_2, channel['channel_id'])
    result = channels_list_v1(user_id_2)['channels']

    assert len(result) == 1

@clear
def test_invalid_userid():
    with pytest.raises(AccessError) as e: 
        channel_join_v1(-1, 0)
        assert 'User ID is invalid' in str(e.value)
    
    clear_v1()
    with pytest.raises(AccessError) as e: 
        channel_join_v1(5, 0)
        assert 'User ID is invalid' in str(e.value)
    
@clear
def test_invalid_channelID(helper):
    helper.register_users(1)
    #helper.create_channels(1)
    invalid_id = 10
    with pytest.raises(InputError) as e: 
        channel_join_v1(1, invalid_id)
        assert 'Channel ID is invalid' in str(e.value)

@clear
def test_access_to_private():
    user = auth_register_v1(email='bobsmith1@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    auth_user_id = user['auth_user_id']

    user_2 = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob2',
                                name_last='smith2')
    user_id_2 = user_2['auth_user_id']

    channels_create_v1(auth_user_id, "channel1", False)
    channel_2 = channels_create_v1(auth_user_id, "channel2", False)

    channel_id_2 = channel_2['channel_id']

    with pytest.raises(AccessError) as e: 
        channel_join_v1(user_id_2, channel_id_2)
        assert 'Cannot access the private channel' in str(e.value)


@clear
def test_channel_not_exist(helper):
    helper.register_users(1)
    channel_id = 1
    with pytest.raises(InputError) as e: 
        channel_join_v1(1, channel_id)
        assert f'Channel with ID {channel_id} does not exist' in str(e.value)

@clear
def test_already_member_of_channel():
    user = auth_register_v1(email='bobsmith1@gmail.com',
                                password='12345678',
                                name_first='bob',
                                name_last='smith')
    user_2 = auth_register_v1(email='bobsmith2@gmail.com',
                                password='12345678',
                                name_first='bob2',
                                name_last='smith2')

    auth_user_id = user['auth_user_id']
    user_id_2 = user_2['auth_user_id']

    channel = channels_create_v1(auth_user_id, "channel1", True)
    channel_id = channel['channel_id']

    channel_join_v1(user_id_2, channel_id)
    with pytest.raises(InputError) as e: 
        channel_join_v1(user_id_2, channel_id)
        assert 'The user is already in the channel' in str(e.value)
