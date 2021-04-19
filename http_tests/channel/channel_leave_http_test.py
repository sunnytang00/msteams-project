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

    creator_id = user1.json().get('auth_user_id')
    u_id = user2.json().get('auth_user_id')

    ch_id = helper.create_channel(1,token1, 'big fish!', True).json().get('channel_id')
    requests.post(url + "/channel/addowner/v1", json = {
        'token': token1,
        'channel_id' : ch_id,
        'u_id': u_id
    })

    response = requests.post(url + "/channel/leave/v1", json = {
        'token': token1,
        'channel_id' : ch_id
    })
    assert response.status_code == 200

    url2 = urlencode({"token": token2, "channel_id": ch_id})

    channel = requests.get(url + 'channel/details/v2?' + url2).json()

    assert creator_id not in [user['u_id'] for user in channel['owner_members']] \
           and creator_id not in [user['u_id'] for user in channel['all_members']]


@clear
def test_invalid_channel_id(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    ch_id = 10

    response = requests.post(url + "/channel/leave/v1", json = {
        'token': token1,
        'channel_id' : ch_id
    })
    assert response.status_code == 400

@clear
def test_auth_user_not_member(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    ch_id = helper.create_channel(2,token2, 'big fish!', True).json().get('channel_id')
    response = requests.post(url + "/channel/leave/v1", json = {
        'token': token1,
        'channel_id' : ch_id
    })
    assert response.status_code == 403


