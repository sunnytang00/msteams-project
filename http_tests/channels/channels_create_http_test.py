import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper

@clear
def test_channels_create_basic(helper):
    ##register a user first
    token = helper.register_user(1).json().get('token')
    assert token

    response = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1',
        'is_public': True
    })
    assert response.status_code == 200

    # reading data from response
    data = response.json()
    channel_id = data.get('channel_id')

    assert channel_id == 1

@clear
def test_name_too_long(helper):
    token = helper.register_user(1).json().get('token')
    assert token

    response = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1' * 20,
        'is_public': True
    })

    assert response.status_code == 400