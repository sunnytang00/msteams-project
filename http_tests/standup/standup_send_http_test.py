import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode
import time

@clear
def test_invalid_channel(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = 10
    msg = "1234"
    
    response = requests.post(url + "standup/send/v1", json = {
        "token": token1,
        "channel_id": ch_id,
        "message" : msg
    })
    assert response.status_code == 400

@clear
def test_msg_too_long(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = helper.create_channel(1, token1, 'big fish', True).json().get('channel_id')

    msg = "1" * 1001

    response = requests.post(url + "standup/send/v1", json = {
        "token": token1,
        "channel_id": ch_id,
        "message" : msg
    })
    assert response.status_code == 400

@clear
def test_standup_inactive(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = helper.create_channel(1, token1, 'big fish', True).json().get('channel_id')

    msg = "1"

    response = requests.post(url + "standup/send/v1", json = {
        "token": token1,
        "channel_id": ch_id,
        "message" : msg
    })
    assert response.status_code == 400

@clear
def test_not_member_of_channel(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    ch_id = helper.create_channel(2, token2, 'big fish', True).json().get('channel_id')

    msg = "1234"

    response = requests.post(url + "standup/send/v1", json = {
        "token": token1,
        "channel_id": ch_id,
        "message" : msg
    })
    assert response.status_code == 403