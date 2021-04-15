import requests
import time
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

@clear
def test_time_created(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    ch_id = helper.create_channel(1,token1, 'big fish!', True).json().get('channel_id')
    requests.post(url + 'message/send/v2', json = {
        'token' : token1,
        'channel_id' : ch_id,
        'message' : 'first message'
    })

    expected_time = int(time.time())

    url2 = urlencode({"token": token1, "channel_id" : ch_id,  "start": 0})

    response = requests.get(url + "/channel/messages/v2?" + url2)
    assert response.status_code == 200

    msgs = response.json()
    actual_time = msgs['messages'][0]['time_created']
    assert expected_time == actual_time


@clear
def test_pagination(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    ch_id = helper.create_channel(1,token1, 'big fish!', True).json().get('channel_id')
    url2 = urlencode({"token": token1, "channel_id": ch_id, "start": 0})

    response = requests.get(url + "/channel/messages/v2?" + url2)
    assert response.status_code ==  200

    msgs = response.json()

    assert msgs.get('start') == 0 and msgs.get('end') == -1 

@clear
def test_invalid_channel_id(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = 10

    url2 = urlencode({"token": token1, "channel_id": ch_id, "start": 0})

    response = requests.get(url + "/channel/messages/v2?" + url2)
    assert response.status_code ==  400

@clear
def test_invalid_start(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    ch_id = helper.create_channel(1,token1, 'big fish!', True).json().get('channel_id')
    url2 = urlencode({"token": token1, "channel_id": ch_id, "start": 100})

    response = requests.get(url + "/channel/messages/v2?" + url2)
    assert response.status_code ==  400

@clear
def test_user_not_member(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    ch_id = helper.create_channel(1,token1, 'big fish!', True).json().get('channel_id')
    url2 = urlencode({"token": token2, "channel_id": ch_id, "start": 0})

    response = requests.get(url + "/channel/messages/v2?" + url2)
    assert response.status_code ==  403
