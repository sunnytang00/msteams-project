import requests
from json import loads
from src.base.config import url

def test_register_basic():

    auth_user_id = 1
    response = requests.post(url + 'channels/create/v2', json = {
        #'email' : 'harrypotter@gmail.com',
       # 'password' : 'dumbledore',
        #'name_first' : 'harry',
       # 'name_last' : 'potter'
        'channel_id': 1,
        'name': 'channel_test1',
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'messages': [],
        'is_public': True
    })

    status_code = response.status_code

    # reading data from response
    data = response.json()
    channel_id = data.get('channel_id')


    assert channel_id == 1
    assert status_code == 201