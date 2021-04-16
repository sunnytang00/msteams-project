import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.base.helper import create_dm_name
import urllib

@clear
def test_invalid_channel(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = 10

    length = 1

    response = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id
        'length': length
    })
    assert response.status_code == 400

@clear
def test_standup_already_started(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = helper.create_channel(1, token1, 'big fish', True).json().get('channel_id')

    length = 2

    response = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id
        'length': length
    })
    assert response.status_code == 200

    response = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id
        'length': length
    })
    assert response.status_code == 400

@clear
def test_not_member_in_channel(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2
    u_id = user2.json().get('auth_user_id')

    ch_id = helper.create_channel(2, token2, 'big fish', True).json().get('channel_id')

    length = 1

    response = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id
        'length': length
    })
    assert response.status_code == 403