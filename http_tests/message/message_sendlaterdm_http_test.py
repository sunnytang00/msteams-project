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

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : []
    })

    dm_id = dm.json().get('dm_id')
    msg = "1234"

    time_sent = int(time.time()) + 1
    response = requests.post(url + "message/sendlaterdm/v1", json ={
        'token': token1,
        'dm_id': dm_id,
        'message' : msg,
        'time_sent' : time_sent
    })
    assert response.status_code == 200
    message_id = response.json()
    time.sleep(2)
    
    url2 = urlencode({'token': token1, 'dm_id': dm_id, 'start': 0})

    msgs = requests.get(url + "dm/messages/v1?" + url2).json()
    assert len(msgs.get('messages')) == 1 and msgs.get('messages')[0].get('message') == "1234" and \
        message_id.get('message_id') == msgs.get('messages')[0].get('message_id')

@clear
def test_invalid_DM(helper):
    user1 = helper.register_user(1)
    token1 = user1.json().get('token')
    assert token1

    dm_id = 10 
    msg = "1234"
    time_sent = int(time.time()) + 10
    response = requests.post(url + "message/sendlaterdm/v1", json ={
        'token': token1,
        'dm_id': dm_id,
        'message' : msg,
        'time_sent' : time_sent
    })
    assert response.status_code == 400

@clear
def test_msg_too_long(helper):
    user1 = helper.register_user(1)
    token1 = user1.json().get('token')
    assert token1

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : []
    })

    dm_id = dm.json().get('dm_id')
    msg = "1" * 1001
    time_sent = int(time.time()) + 10
    response = requests.post(url + "message/sendlaterdm/v1", json ={
        'token': token1,
        'dm_id': dm_id,
        'message' : msg,
        'time_sent' : time_sent
    })
    assert response.status_code == 400

@clear
def test_past_time(helper):
    user1 = helper.register_user(1)
    token1 = user1.json().get('token')
    assert token1

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : []
    })

    dm_id = dm.json().get('dm_id')
    msg = "1234"
    time_sent = int(time.time()) - 10
    response = requests.post(url + "message/sendlaterdm/v1", json ={
        'token': token1,
        'dm_id': dm_id,
        'message' : msg,
        'time_sent' : time_sent
    })
    assert response.status_code == 400

@clear
def test_not_member_of_DM(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token2,
        'u_ids' : []
    })

    dm_id = dm.json().get('dm_id')
    msg = "1234"
    time_sent = int(time.time()) + 10
    response = requests.post(url + "message/sendlaterdm/v1", json ={
        'token': token1,
        'dm_id': dm_id,
        'message' : msg,
        'time_sent' : time_sent
    })
    assert response.status_code == 403