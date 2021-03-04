import pytest
import time
from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper

def test_time_created():
    clear_v1()
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    channel = channels_create_v1(user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    unix_timestamp = int(time.time()) # round to the neareast second

    result = channel_messages_v1(auth_user_id=user_id, channel_id=channel_id, start=0)
    result_unix_timestamp = result['messages'][0]['time_created']
    
    assert unix_timestamp == result_unix_timestamp

def test_pagination():
    clear_v1()
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    channel = channels_create_v1(user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    result = channel_messages_v1(auth_user_id=user_id, channel_id=channel_id, start=0)
    result_start = result['start']
    result_end = result['end']
    
    assert result_start == 0 and result_end == -1

def test_invalid_channel_id():
    clear_v1()

    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    invalid_channel_id = 40

    with pytest.raises(InputError) as e: 
        channel_messages_v1(auth_user_id=user_id, channel_id=invalid_channel_id, start=0)
        assert f'Channel ID {invalid_channel_id} is not a valid channel' in str(e)

def test_invalid_start():
    clear_v1()

    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='42flshjfzhh8',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    channel = channels_create_v1(user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    invalid_start = 100

    with pytest.raises(InputError) as e: 
        channel_messages_v1(auth_user_id=user_id, channel_id=channel_id, start=invalid_start)
        assert f'Start {invalid_start} is greater than the total number of messages in the channel.' in str(e)

# TODO: AccessError
      