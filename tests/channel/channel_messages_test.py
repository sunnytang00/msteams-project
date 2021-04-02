import pytest
import time
from src.base.channel import channel_messages_v1
from src.base.channels import channels_create_v1
from src.base.error import InputError, AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from tests.helper import helper, clear
from src.base.message import message_send_v1

@clear
def test_time_created():
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    channel = channels_create_v1(auth_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    message_send_v1(auth_user_id, channel_id, 'test message')

    unix_timestamp = int(time.time()) # round to the neareast second

    result = channel_messages_v1(auth_user_id=auth_user_id, channel_id=channel_id, start=0)
    result_unix_timestamp = result['messages'][0]['time_created']
    
    assert unix_timestamp == result_unix_timestamp

@clear
def test_pagination():
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    channel = channels_create_v1(auth_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    result = channel_messages_v1(auth_user_id=auth_user_id, channel_id=channel_id, start=0)
    result_start = result['start']
    result_end = result['end']
    
    assert result_start == 0 and result_end == -1

@clear
def test_invalid_channel_id():
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    invalid_channel_id = 40

    with pytest.raises(InputError) as e: 
        channel_messages_v1(auth_user_id=auth_user_id, channel_id=invalid_channel_id, start=0)
        assert f'Channel ID {invalid_channel_id} is not a valid channel' in str(e)

@clear
def test_invalid_start():
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    channel = channels_create_v1(auth_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    invalid_start = 100

    with pytest.raises(InputError) as e: 
        channel_messages_v1(auth_user_id=auth_user_id, channel_id=channel_id, start=invalid_start)
        assert f'Start {invalid_start} is greater than the total number of messages in the channel.' in str(e)

@clear
def test_user_not_member(helper):
    helper.register_users(10)

    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    auth_user_id = user['auth_user_id']

    channel = channels_create_v1(10, "Cat Society", True)
    channel_id = channel['channel_id']

    with pytest.raises(AccessError) as e: 
        channel_messages_v1(auth_user_id=auth_user_id, channel_id=channel_id, start=0)
        assert f'Authorised user {auth_user_id} is not a member of channel with channel_id {channel_id}' in str(e)