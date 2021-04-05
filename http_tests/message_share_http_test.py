import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

@clear
def test_share_dm(helper):
    """Add and remove a single user's message from a dm"""
    # no optional message
    user1 = helper.register_user(1)
    token1 = user1.json().get('token')
    assert token1

    dm = requests.post(url + "/dm/create/v1", json = {
        'token': token1,
        'u_ids': []
    })
    dm_id = dm.json().get('dm_id')
    assert dm_id == 1

    og_message = "I like shrimps"

    #message_info = message_senddm_v1(auth_user_id, dm_id, og_message)
    message_info = requests.post(url + "/message/senddm/v1", json = {
        'token': token1,
        'dm_id': dm_id,
        'message' : og_message
    })
    og_message_id = message_info.json().get('message_id')

    assert og_message_id == 1

    optional_message = ''

    channel_id = -1
    #message_info = message_share_v1(auth_user_id, og_message_id, optional_message, channel_id, dm_id)
    message_info = requests.post(url + "message/share/v1", json = {
        'token': token1,
        'og_message_id': og_message_id,
        'message' : optional_message,
        'channel_id': channel_id,
        'dm_id': dm_id
    })
    assert message_info.status_code == 201

    shared_message_id = message_info.json().get('shared_message_id')
    assert shared_message_id == 2

    #dm_messages = dm_messages_v1(auth_user_id, dm_id, 0).get('messages')
    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 0})
    dm_messages_data = requests.get(url + "dm/messages/v1?" + url2)
    print(dm_messages_data)
    dm_messages = dm_messages_data.json().get('messages')

    shared_message = dm_messages[0]

    expected = f'{optional_message}\n"""\n{og_message}\n"""'
    assert dm_messages[0].get('message') == expected

    #optional message
    optional_message = '1'
    #message_info = message_share_v1(auth_user_id, og_message_id, optional_message, channel_id, dm_id)
    message_info = requests.post(url + "message/share/v1", json = {
        'token': token1,
        'og_message_id': og_message_id,
        'message' : optional_message,
        'channel_id': channel_id,
        'dm_id': dm_id
    })
    assert message_info.status_code == 201

    shared_message_id = message_info.json().get('shared_message_id')
    assert shared_message_id == 3
    #dm_messages = dm_messages_v1(auth_user_id, dm_id, 0).get('messages')
    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 0})
    dm_messages_data = requests.get(url + "/dm/messages/v1?" + url2)
    dm_messages = dm_messages_data.json().get('messages')
    
    shared_message = dm_messages[0]
    
    expected = f'{optional_message}\n"""\n{og_message}\n"""'
    assert dm_messages[0].get('message') == expected