import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.helper import token_to_auth_user_id
from urllib.parse import urlencode

@clear
def test_react_route(helper):
    #Creating user 1
    user_1 = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    user_info =  user_1.json()
    auth_user_id_1 = user_info.get('auth_user_id')
    token_1 = user_info.get('token')
    assert auth_user_id_1 == 1

    #Creating user 2
    user_2 = requests.post(url + 'auth/register/v2', json = {
        'email' : 'Spiderman@gmail.com',
        'password' : 'yesdumbledore',
        'name_first' : 'Spider',
        'name_last' : 'Man'
    })

    user_info =  user_2.json()
    auth_user_id_2 = user_info.get('auth_user_id')
    token_2 = user_info.get('token')
    assert auth_user_id_2 == 2

    #Create channel
    channel = requests.post(url + 'channels/create/v2', json = {
        'token': token_1,
        'name': 'Super heroes',
        'is_public': True
    })

    channel_info = channel.json()
    channel_id = channel_info.get('channel_id')
    assert channel_id == 1

    #Channel invite
    response = requests.post(url + "/channel/invite/v2", json = {
        'token': token_1,
        'channel_id': channel_id,
        'u_id': auth_user_id_2

    })
    assert response.status_code == 200

    #Create message
    message = requests.post(url + 'message/send/v2', json = {
        'token' : token_1,
        'channel_id' : channel_id,
        'message' : "Writing tests is so fun !!!"

    })
    message_id = message.json().get('message_id')

    assert message.status_code == 200

    #Asking for messages in the data
    url2 = urlencode({"token": token_1, "channel_id" : channel_id,  "start": 0})
    response = requests.get(url + "/channel/messages/v2?" + url2)
    
    assert response.status_code == 200

    messages = response.json().get('messages')

    #React to message
    response = requests.post(url + "message/react/v1", json = {
        'token': token_2,
        'message_id': message_id,
        'react_id': messages[0].get('reacts')[0].get('react_id'),
    })
    #Check if the user reacted to the message.
    assert messages[0].get('reacts')[0].get('is_this_user_reacted') == True