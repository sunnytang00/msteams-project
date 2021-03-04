import pytest
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper

def test_valid_input():
    clear_v1()
    user = auth_register_v1(email='bobsmith@gmail.com',
                                password='FVn4HTWEsz8k6Msf',
                                name_first='Bob',
                                name_last='Smith')
    user_id = user['auth_user_id']

    channel = channels_create_v1(user_id, 'Cat Society', True)
    channel_id = channel['channel_id']

    result = channel_details_v1(auth_user_id=user_id, channel_id=channel_id)
    
    assert result == {'name': 'Cat Society', 'owner_members': [user_id], 'all_members': [user_id]}