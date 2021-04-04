import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.base.helper import token_to_auth_user_id

@clear
def test_valid_input(helper):
    user1 = helper.register_user(1)
    helper.register_uesr(2)
    
    token1 = user1.json().get('token')

    ch1 = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'channel_test1',
        'is_public': True
    })
    ch2 = requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'channel_test2',
        'is_public': True
    })
    ch1_id = ch1.json().get('channel_id')
    ch2_id = ch2.json().get('channel_id')
    
    channels = requests.get(url + 'channels/listall/v2?token=' + token1).json()

    assert len(channels) == 2
'''
@clear
def test_invalid_email():
    # TODO:not sure if this is exactly right gotta check
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter_is_cool',
        'password' : 'dubledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    assert response.status_code == 400
'''