import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.helper import token_to_auth_user_id

@clear
def test_valid_input(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    helper.create_channel(1,token1, 'big fish!', True)
    helper.create_channel(1,token1, 'big fish2!', True)
    channels = requests.get(url + 'channels/listall/v2?token=' + token1).json()

    assert len(channels['channels']) == 2

@clear
def test_private_channel_exists(helper):
    token1 = helper.register_user(1).json().get('token')
    token2 = helper.register_user(2).json().get('token')

    assert token1
    assert token2

    r1 = helper.create_channel(1, token1) # r for response
    r2 = helper.create_channel(value=2, token=token1, is_public=False)

    ch1_id = r1.json().get('channel_id')
    ch2_id = r2.json().get('channel_id')

    channels = requests.get(url + 'channels/listall/v2?token=' + token2).json()

    ch_ids = [channel['channel_id'] for channel in channels['channels']]
    assert ch1_id in ch_ids and ch2_id not in ch_ids


