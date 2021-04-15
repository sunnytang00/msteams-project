import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

@clear 
def test_valid_input(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    auth_user_id = user1.json().get('auth_user_id')
    assert token1

    ch_id = helper.create_channel(1,token1, 'big fish!', True).json().get('channel_id')
    url2 = urlencode({"token": token1, "channel_id": ch_id})

    response = requests.get(url + 'channel/details/v2?' + url2)
    assert response.status_code == 200
    
    channel = response.json()
    assert auth_user_id in [users['u_id'] for users in channel['all_members']]

@clear
def test_invalid_channel(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    ch_id = 10

    url2 = urlencode({"token": token1, "channel_id": ch_id})

    response = requests.get(url + 'channel/details/v2?' + url2)
    assert response.status_code == 400
    
@clear
def test_user_not_authorised(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    ch_id = helper.create_channel(1,token1, 'big fish!', True).json().get('channel_id')
    url2 = urlencode({"token": token2, "channel_id": ch_id})

    response = requests.get(url + 'channel/details/v2?' + url2)
    assert response.status_code == 403
