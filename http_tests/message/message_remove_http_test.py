import requests
from json import loads
from http_tests.helper import helper, clear
from src.config import url
from src.data.helper import get_message_count
from urllib.parse import urlencode

@clear
def test_basic(helper):
    #creating 1st user.
    response = helper.register_user(1)

    assert response.status_code == 200

    data = response.json()
    token_0 = data.get('token')

    #creating 2nd user.
    response = helper.register_user(2)

    assert response.status_code == 200

    data = response.json()
    auth_user_id_1 = data.get('auth_user_id')
    
    #creating 3rd user.
    response = helper.register_user(3)

    assert response.status_code == 200

    data = response.json()
    auth_user_id_2 = data.get('auth_user_id')

    #creating channel.
    response = helper.create_channel(1, token_0)

    assert response.status_code == 200

    data = response.json()
    channel_id = data['channel_id']

    #Inviting 2nd user and 3rd user to the channel.
    response = requests.post(url + "/channel/invite/v2", json = {
        'token': token_0,
        'channel_id': channel_id,
        'u_id': auth_user_id_1,
    })

    assert response.status_code == 200
    
    response = requests.post(url + "/channel/invite/v2", json = {
        'token': token_0,
        'channel_id': channel_id,
        'u_id': auth_user_id_2,
    })
    
    assert response.status_code == 200


    #Create a message.
    response = requests.post(url + "message/send/v2", json = {
        'token': token_0,
        'channel_id': channel_id,
        'message': "Hello everyone!",
    })

    assert response.status_code == 200    
    #remove the message

    data = response.json()
    message_id = data['message_id']

    response = requests.delete(url + "message/remove/v1", json = {
        'token': token_0,
        'message_id': message_id,
    })

    assert response.status_code == 200

    #check if message is deleted.
    url2 = urlencode({"token": token_0, "channel_id": channel_id, "start": 0})
    
    response = requests.get(url + "channel/messages/v2?" + url2)

    assert response.status_code == 200 

    data = response.json()
    messages = data['messages']

    assert len(messages) == 0