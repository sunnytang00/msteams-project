import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.helper import create_dm_name

@clear

def test_basic(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')

    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })

    dm_info = dm.json()
    dm_id = dm_info.get('dm_id')

    msg_senddm = requests.post(url + 'message/senddm/v1', json = {
        'token' : token,
        'dm_id' : dm_id,
        'message' : 'i hope this works'
    })

    msg_dm_info = msg_senddm.json()
    assert msg_dm_info.get('message_id') == 1

@clear

def test_input_error(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')

    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })

    dm_info = dm.json()
    dm_id = dm_info.get('dm_id')

    response = requests.post(url + 'message/senddm/v1', json = {
        'token' : token,
        'dm_id' : dm_id,
        'message' : 'a' * 1001
    })

    assert response.status_code == 400

@clear

def test_access_error(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')
    token3 = data3.get('token')

    u_id2 = data2.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    dm_info = dm.json()
    dm_id = dm_info.get('dm_id')

    response = requests.post(url + 'message/senddm/v1', json = {
        'token' : token3,
        'dm_id' : dm_id,
        'message' : 'a' * 1000
    })

    assert response.status_code == 403




