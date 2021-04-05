import requests
import time
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

@clear
def test_no_msg_in_dm(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : []
    })
    dm_id = dm.json().get('dm_id')

    expected = {'messages': [], 'start': 0, 'end': -1}

    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 0})

    response = requests.get(url + "/dm/messages/v1?" + url2)
    assert response.status_code == 200

    actual = response.json()

    assert expected == actual



@clear
def test_invalid_dm_id(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    dm_id = 10
    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 0})

    response = requests.get(url + "/dm/messages/v1?" + url2)
    assert response.status_code == 400

@clear
def test_invalid_start(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : []
    })
    dm_id = dm.json().get('dm_id')

    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 100})

    response = requests.get(url + "/dm/messages/v1?" + url2)
    assert response.status_code == 400

@clear
def test_auth_user_not_member(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)

    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : []
    })
    dm_id = dm.json().get('dm_id')


    url2 = urlencode({"token": token2, "dm_id": dm_id, "start": 0})

    response = requests.get(url + "/dm/messages/v1?" + url2)
    assert response.status_code == 403



#tests below requires message_senddm
#maybe could import the base version of message_senddm temporarily?

@clear
def test_few_msgs_in_dm(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : []
    })
    dm_id = dm.json().get('dm_id')

    msgs = ['1', '2', '3', '4', '5']

    for msg in msgs:
        requests.post(url + 'message/senddm/v1', json = {
            'token': token1,
            'dm_id': dm_id,
            'message': msg
        })

    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 0})

    response = requests.get(url + "/dm/messages/v1?" + url2)
    assert response.status_code == 200

    messages = response.json()
    
    assert messages['messages'][0]['message_id'] == 5 and messages['end'] == -1

def useless_message(quantity: int) -> list:
    i = 0
    msgs = []
    while i < quantity:
        msgs.append("nothing")
        i += 1
    return msgs

@clear
def test_many_msgs_in_dm(helper):
    user1 = helper.register_user(1)
    
    token1 = user1.json().get('token')
    assert token1

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : []
    })
    dm_id = dm.json().get('dm_id')

    msgs = []
    msgs.append("orange")
    msgs.extend(useless_message(50))
    msgs.append("last")

    for msg in msgs:
        requests.post(url + 'message/senddm/v1', json = {
            'token': token1,
            'dm_id': dm_id,
            'message': msg
        })

    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 0})

    response = requests.get(url + "/dm/messages/v1?" + url2)
    assert response.status_code == 200

    messages = response.json()
    
    assert "last" in [msg['message'] for msg in messages['messages']] \
            and "orange" not in [msg['message'] for msg in messages['messages']] \
            and messages['end'] == 50
