import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode
import time
@clear
def test_valid_input(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    u_id = user1.json().get('auth_user_id')

    ch_id = helper.create_channel(1, token1, 'big fish', True).json().get('channel_id')
    length = 1

    url_profile = urlencode({'token': token1, 'u_id': u_id})
    handle_str = requests.get(url + "user/profile/v2?" + url_profile).json().get('user').get('handle_str')
    response = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id,
        'length': length
    }) 
    assert response.status_code == 200
    time_finish = response.json().get('time_finish')

    expected = int(time.time()) + length

    requests.post(url + "standup/send/v1", json = {
        'token': token1,
        'channel_id': ch_id,
        'message': '123'
    })

    requests.post(url + "standup/send/v1", json = {
        'token': token1,
        'channel_id': ch_id,
        'message': '1234'
    })

    requests.post(url + "standup/send/v1", json = {
        'token': token1,
        'channel_id': ch_id,
        'message': '@' + handle_str + ' ' + '1234'
    })

    time.sleep(2)

    url_message = urlencode({'token': token1, 'channel_id': ch_id, 'start': 0})
    msgs = requests.get(url + "channel/messages/v2?" + url_message).json()

    notifications = requests.get(url + "notifications/get/v1?token=" + token1).json()

    assert len(notifications) == 1
    assert len(msgs.get('messages')) == 1
    assert time_finish == expected

@clear
def test_invalid_channel(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = 10

    length = 1

    response = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id,
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
        'channel_id': ch_id,
        'length': length
    })
    assert response.status_code == 200

    response = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id,
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

    ch_id = helper.create_channel(2, token2, 'big fish', True).json().get('channel_id')

    length = 1

    response = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id,
        'length': length
    })
    assert response.status_code == 403