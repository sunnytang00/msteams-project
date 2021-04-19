import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
import urllib
@clear

def test_user_stats_basic(helper):
    response1 = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data1 = response1.json()
    token1 = data1.get('token')
    data2 = response2.json()
    token2 = data2.get('token')
    data3 = response3.json()
    token3 = data3.get('token')

    requests.post(url + 'channels/create/v2', json = {
        'token': token1,
        'name': 'channel_test1',
        'is_public': True
    })

    requests.post(url + 'channels/create/v2', json = {
        'token': token2,
        'name': 'testing123',
        'is_public': True
    })

    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    dm1 = requests.post(url + 'dm/create/v1', json = {
        'token' : token1,
        'u_ids' : [u_id2]
    })

    dm2 = requests.post(url + 'dm/create/v1', json = {
        'token' : token2,
        'u_ids' : [u_id3]
    })

    dm_info1 = dm1.json()
    assert dm_info1.get('dm_id') == 1
    dm_info2 = dm2.json()
    assert dm_info2.get('dm_id') == 2

    requests.post(url + 'message/senddm/v1', json = {
        'token' : token1,
        'dm_id' : dm_info1.get('dm_id'),
        'message' : 'i hope this works'
    })

    requests.post(url + 'message/senddm/v1', json = {
        'token' : token2,
        'dm_id' : dm_info2.get('dm_id'),
        'message' : 'i hope this works again'
    })

    queryString = urllib.parse.urlencode({
        'token' : token1
    })

    stats = requests.get(url + f'user/stats/v1?{queryString}')
    user_stats = stats.json().get('user_stats')
    assert user_stats.get('channels_joined')[0].get('num_channels_joined') == 1
    assert len(user_stats.get('channels_joined')[0].get('time_stamp')) == 1
    assert user_stats.get('dms_joined')[0].get('num_dms_joined') == 1
    assert len(user_stats.get('dms_joined')[0].get('time_stamp')) == 1
    assert user_stats.get('messages_sent')[0].get('num_messages_sent') == 1
    assert len(user_stats.get('messages_sent')[0].get('time_stamp')) == 1
    assert user_stats.get('involvement_rate') == 0.5

    queryString = urllib.parse.urlencode({
        'token' : token3
    })

    stats = requests.get(url + f'user/stats/v1?{queryString}')
    user_stats = stats.json().get('user_stats')
    assert user_stats.get('channels_joined')[0].get('num_channels_joined') == 0
    assert len(user_stats.get('channels_joined')[0].get('time_stamp')) == 0
    assert user_stats.get('dms_joined')[0].get('num_dms_joined') == 1
    assert len(user_stats.get('dms_joined')[0].get('time_stamp')) == 1
    assert user_stats.get('messages_sent')[0].get('num_messages_sent') == 0
    assert len(user_stats.get('messages_sent')[0].get('time_stamp')) == 0
    assert user_stats.get('involvement_rate') == 1/6