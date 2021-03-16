import requests
from json import loads
from src.base.config import url

def test_channels_create_basic():
    ##register a user first
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter2@gmail1.com',
        'password' : 'dumbledore2',
        'name_first' : 'harry2',
        'name_last' : 'potter2'
    })
    status_code = response.status_code
    assert status_code == 201

    user = response.json()
    auth_user_id = user['auth_user_id']

    response = requests.post(url + 'channels/create/v2', json = {
        'auth_user_id': auth_user_id,
        'name': 'channel_test1',
        'is_public': True
    })

    status_code = response.status_code
    # reading data from response
    data = response.json()
    channel_id = data.get('channel_id')

    assert channel_id == 1
    assert status_code == 201