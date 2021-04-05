import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper

@clear
def test_sendmessage_basic():
    user = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    user_info =  user.json()
    auth_user_id = user_info.get('auth_user_id')
    token = user_info.get('token')
    assert auth_user_id == 1

    channel = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1',
        'is_public': True
    })

    channel_info = channel.json()
    channel_id = channel_info.get('channel_id')
    assert channel_id == 1

    message = requests.post(url + 'message/send/v2', json = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : 'i hope this works'

    })
    
    message_info = message.json()
    message_id = message_info.get('message_id')
    assert message_id == 1
  
@clear
def test_input_error():
    user = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    user_info =  user.json()
    auth_user_id = user_info.get('auth_user_id')
    token = user_info.get('token')
    assert auth_user_id == 1

    channel = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1',
        'is_public': True
    })

    channel_info = channel.json()
    channel_id = channel_info.get('channel_id')
    assert channel_id == 1

    message = requests.post(url + 'message/send/v2', json = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : 'a' * 1001

    })
    
    assert message.status_code == 400

@clear
def test_access_error(helper):
    user = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    user_info =  user.json()
    auth_user_id = user_info.get('auth_user_id')
    token = user_info.get('token')
    assert auth_user_id == 1


    channel = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1',
        'is_public': True
    })

    channel_info = channel.json()
    channel_id = channel_info.get('channel_id')
    assert channel_id == 1

    response = helper.register_user(2)
    data = response.json()
    token2 = data.get('token')

    message = requests.post(url + 'message/send/v2', json = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : 'a' * 1000

    })
    
    assert message.status_code == 403
