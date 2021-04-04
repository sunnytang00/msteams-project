import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.base.helper import token_to_auth_user_id

@clear
def test_valid_input(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    ch1 = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'channel_test1',
        'is_public': True
    })
    ch2 = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'channel_test2',
        'is_public': False
    })
    
    ch1_id = ch1.json().get('channel_id')
    ch2_id = ch2.json().get('channel_id')

    channels = requests.get(url + 'channels/list/v2?token=' + token1).json()

    ch_ids = [channel['channel_id'] for channel in channels['channels']]
    assert ch1_id in ch_ids and ch2_id in ch_ids

@clear
def test_multiple_member_exists(helper):
    token1 = helper.register_user(1).json().get('token')
    token2 = helper.register_user(2).json().get('token')

    assert token1
    assert token2

    ch1 = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'channel_test1',
        'is_public': True
    })
    ch2 = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'channel_test2',
        'is_public': False
    })
    ch1_id = ch1.json().get('channel_id')
    ch2_id = ch2.json().get('channel_id')

    channels = requests.get(url + 'channels/list/v2?token=' + token2).json()

    ch_ids = [channel['channel_id'] for channel in channels['channels']]
    assert ch1_id not in ch_ids and ch2_id not in ch_ids

@clear
def test_no_channel_exists(helper):
    token1 = helper.register_user(1).json().get('token')

    assert token1
    channels = requests.get(url + 'channels/list/v2?token=' + token2).json()

    ch_ids = [channel['channel_id'] for channel in channels['channels']]
    assert ch_ids = []