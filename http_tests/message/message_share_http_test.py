import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

#@clear
#def test_share_dm(helper):
#    """Add and remove a single user's message from a dm"""
#    # no optional message
#    user1 = helper.register_user(1)
#    token1 = user1.json().get('token')
#    assert token1
#
#    dm = requests.post(url + "/dm/create/v1", json = {
#        'token': token1,
#        'u_ids': []
#    })
#    dm_id = dm.json().get('dm_id')
#    assert dm_id == 1
#
#    og_message = "I like shrimps"
#
#    
#    message_info = requests.post(url + "/message/senddm/v1", json = {
#        'token': token1,
#        'dm_id': dm_id,
#        'message' : og_message
#    })
#    og_message_id = message_info.json().get('message_id')
#
#    assert og_message_id == 1
#
#    optional_message = ''
#
#    channel_id = -1
#    
#    message_info = requests.post(url + "message/share/v1", json = {
#        'token': token1,
#        'og_message_id': og_message_id,
#        'message' : optional_message,
#        'channel_id': channel_id,
#        'dm_id': dm_id
#    })
#    assert message_info.status_code == 200
#
#    shared_message_id = message_info.json().get('shared_message_id')
#    assert shared_message_id == 2
#
#    
#    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 0})
#    dm_messages_data = requests.get(url + "dm/messages/v1?" + url2)
#    dm_messages = dm_messages_data.json().get('messages')
#
#
#    expected = f'{optional_message}\n"""\n{og_message}\n"""'
#    assert dm_messages[0].get('message') == expected
#
#    #optional message
#    optional_message = '1'
#    
#    message_info = requests.post(url + "message/share/v1", json = {
#        'token': token1,
#        'og_message_id': og_message_id,
#        'message' : optional_message,
#        'channel_id': channel_id,
#        'dm_id': dm_id
#    })
#    assert message_info.status_code == 200
#
#    shared_message_id = message_info.json().get('shared_message_id')
#    assert shared_message_id == 3
#    
#    url2 = urlencode({"token": token1, "dm_id": dm_id, "start": 0})
#    dm_messages_data = requests.get(url + "/dm/messages/v1?" + url2)
#    dm_messages = dm_messages_data.json().get('messages')
#    
#    
#    expected = f'{optional_message}\n\n"""\n{og_message}\n"""'
#    assert dm_messages[0].get('message') == expected

@clear
def test_user_is_not_member(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    dm = requests.post(url + "/dm/create/v1", json = {
        'token': token1,
        'u_ids': []
    })
    dm_id = dm.json().get('dm_id')
    assert dm_id == 1

    og_message = "I like shrimps"

    
    message_info = requests.post(url + "/message/senddm/v1", json = {
        'token': token1,
        'dm_id': dm_id,
        'message' : og_message
    })
    og_message_id = message_info.json().get('message_id')

    assert og_message_id == 1

    optional_message = ''

    channel_id = -1
    
    message_info = requests.post(url + "message/share/v1", json = {
        'token': token2,
        'og_message_id': og_message_id,
        'message' : optional_message,
        'channel_id': channel_id,
        'dm_id': dm_id
    })
    assert message_info.status_code == 403