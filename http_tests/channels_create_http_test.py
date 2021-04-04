import requests
from json import loads
from src.config import url

def test_channels_create_basic():
    ##register a user first
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter2@gmail1.com',
        'password' : 'dumbledore2',
        'name_first' : 'harry2',
        'name_last' : 'potter2'
    })

    token = response.json().get('token')
    assert token
    response = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1',
        'is_public': True
    })

    status_code = response.status_code
    # reading data from response
    data = response.json()
    channel_id = data.get('channel_id')

    assert channel_id == 1
    assert status_code == 201