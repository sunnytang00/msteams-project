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

    ch_id = helper.create_channel(1, token1, 'big fish', True).json().get('channel_id')
    length = 1

    time_finish_json = requests.post(url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': ch_id,
        'length': length
    }) 
    time_finish = time_finish_json.json().get('time_finish')
    url2 = urlencode({'token': token1, 'channel_id': ch_id})
    response = requests.get(url + "standup/active/v1?" + url2)
    assert response.status_code == 200
    standup_data = response.json()
    
    time.sleep(1)

    assert standup_data.get('is_active') == True and standup_data.get('time_finish') == time_finish

@clear
def test_no_standup_active(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = helper.create_channel(1, token1, 'big fish', True).json().get('channel_id')

    url2 = urlencode({'token': token1, 'channel_id': ch_id})
    response = requests.get(url + "standup/active/v1?" + url2)
    assert response.status_code == 200
    standup_data = response.json()

    assert standup_data.get('is_active') == False and standup_data.get('time_finish') == None

@clear
def test_invalid_channel(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1

    ch_id = 10 
    url2 = urlencode({'token': token1, 'channel_id': ch_id})
    response = requests.get(url + "standup/active/v1?" + url2)
    assert response.status_code == 400