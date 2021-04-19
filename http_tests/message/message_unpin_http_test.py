""" HTTP tests for message/unpin/v1 route """

import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.base.channel import channel_messages_v1

@clear
def test_unpin_pinned_message():
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
        'message' : 'pin me papi'

    })

    message_info = message.json()
    message_id = message_info.get('message_id')

    assert message_id == 1

    requests.put(url + 'message/pin/v1', json = {
        'auth_user_id' : auth_user_id,
        'message_id' : message_id,
    })

    ret = route channel_messages(..)
    ret1 = ret.json()
    print(ret1)

    assert 1 == 2

    assert ret1[0].get('is_pinned') == True

    assert message_info.get('is_pinned') == True

    requests.put(url + 'message/unpin/v1', json = {
        'auth_user_id' : auth_user_id,
        'message_id' : message_id,
    })

    assert message_info.get('is_pinned') == False

@clear
def test_unpin_unpinned_message():
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
        'message' : 'pin me papi'

    })

    message_info = message.json()
    message_id = message_info.get('message_id')

    assert message_id == 1

    response = requests.put(url + 'message/unpin/v1', json = {
        'auth_user_id' : auth_user_id,
        'message_id' : message_id,
    })

    assert response.status_code == 400

@clear
def test_messageid_invalid():
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
        'message' : 'pin me papi'

    })

    message_info = message.json()
    message_id = message_info.get('message_id')
    assert message_id == 1

    requests.post(url + 'message/pin/v1', json = {
        'auth_user_id' : auth_user_id,
        'message_id' : message_id,
    })

    response = requests.post(url + 'message/unpin/v1', json = {
        'auth_user_id' : auth_user_id,
        'message_id' : 4,
    })

    assert response.status_code == 400

@clear
def test_userid_invalid():
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

    user = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter1@gmail.com',
        'password' : 'dumbledoree',
        'name_first' : 'harryy',
        'name_last' : 'potterr'
    })

    user_info1 =  user.json()
    auth_user_id1 = user_info.get('auth_user_id')
    token1 = user_info1.get('token')
    assert auth_user_id1 == 2

    channel = requests.post(url + 'channels/create/v2', json = {
        'token': token,
        'name': 'channel_test1',
        'is_public': True
    })

    channel_info = channel.json()
    channel_id = channel_info.get('channel_id')
    assert channel_id == 1

    requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'channel_test2',
        'is_public': True
    })

    channel_info1 = channel.json()
    channel_id1 = channel_info1.get('channel_id')
    assert channel_id1 == 2

    message = requests.post(url + 'message/send/v2', json = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : 'pin me papi'

    })

    message_info = message.json()
    message_id = message_info.get('message_id')
    assert message_id == 1

    requests.post(url + 'message/pin/v1', json = {
        'auth_user_id' : auth_user_id,
        'message_id' : message_id,
    })

    response = requests.post(url + 'message/unpin/v1', json = {
        'auth_user_id' : auth_user_id1,
        'message_id' : message_id,
    })

    assert response.status_code == 403
