import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

@clear
def test_valid_input(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    ch_id = helper.create_channel(1,token1, 'big fish!', True).json().get('channel_id')
    response = requests.post(url + "/channel/join/v2", json = {
        'token': token2,
        'channel_id': ch_id
    })
    assert response.status_code == 200

    channels = requests.get(url + 'channels/list/v2?token=' + token2).json()

    assert ch_id in (channel['channel_id'] for channel in channels['channels'])

@clear 
def test_invalid_channel(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    ch_id = 10

    response = requests.post(url + "/channel/join/v2", json = {
        'token': token2,
        'channel_id': ch_id
    })

    assert response.status_code == 400

@clear
def test_non_global_owner_access_private(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    ch_id = helper.create_channel(1,token1, 'big fish!', False).json().get('channel_id')
    response = requests.post(url + "/channel/join/v2", json = {
        'token': token2,
        'channel_id': ch_id
    })

    assert response.status_code == 403

@clear
def test_global_owner_access_private(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    ch_id = helper.create_channel(2,token2, 'big fish!', False).json().get('channel_id')
    response = requests.post(url + "/channel/join/v2", json = {
        'token': token1,
        'channel_id': ch_id
    })
    assert response.status_code == 200

    channels = requests.get(url + 'channels/list/v2?token=' + token1).json()

    assert ch_id in (channel['channel_id'] for channel in channels['channels'])


