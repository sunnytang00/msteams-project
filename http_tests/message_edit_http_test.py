import requests
from json import loads
from src.config import url
from http_tests.helper import clear
from src.base.channel import channel_messages_v1
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

    message1 = requests.post(url + 'message/send/v2', json = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : 'sending the second message'

    })

    message1_info = message1.json()
    message1_id = message1_info.get('message_id')
    assert message1_id == 2

    requests.put(url + 'message/edit/v2', json = {
        'token' : token,
        'message_id' : message_id,
        'message' : 'edited the first message'

    })

    messages = channel_messages_v1(auth_user_id, channel_id, 1).get('messages')
    assert messages[1].get('message') == 'edited the first message'
  
