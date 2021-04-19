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
    u_id = data.get('auth_user_id')
    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })

    dm_info = dm.json()
    assert dm_info.get('dm_id') == 1
    assert dm_info.get('dm_name') == create_dm_name([u_id, u_id2, u_id3])

@clear

def test_input_error(helper):

    response = helper.register_user(1)
    response3 = helper.register_user(3)

    data = response.json()
    data3 = response3.json()

    token = data.get('token')
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [4, u_id3]
    })
    
    assert dm.status_code == 400

