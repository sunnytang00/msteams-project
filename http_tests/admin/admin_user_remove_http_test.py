import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

@clear
def test_valid_input(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2
    u_id = user2.json().get('auth_user_id')

    response = requests.delete(url + "admin/user/remove/v1", json ={
        'token': token1,
        'u_id': u_id
    })
    assert response.status_code == 200

    users = requests.get(url + "users/all/v1?token=" + token1).json()

    assert u_id not in [user['u_id'] for user in users['users']]

@clear
def test_invalid_u_id(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1
    u_id = user1.json().get('auth_user_id') + 10

    response = requests.delete(url + "admin/user/remove/v1", json ={
        'token': token1,
        'u_id': u_id
    })
    assert response.status_code == 400

@clear
def test_the_only_owner(helper):
    user1 = helper.register_user(1)

    token1 = user1.json().get('token')
    assert token1
    u_id = user1.json().get('auth_user_id')

    response = requests.delete(url + "admin/user/remove/v1", json ={
        'token': token1,
        'u_id': u_id
    })
    assert response.status_code == 400

@clear
def test_auth_user_not_Dream_owner(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2
    u_id = user1.json().get('auth_user_id')

    response = requests.delete(url + "admin/user/remove/v1", json ={
        'token': token2,
        'u_id': u_id
    })
    assert response.status_code == 403


@clear
def test_remove_only_member_of_channel(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2
    u_id = user2.json().get('auth_user_id')

    ch_id = helper.create_channel(2, token2, 'big fish', True).json().get('channel_id')

    response = requests.delete(url + "admin/user/remove/v1", json ={
        'token': token1,
        'u_id': u_id
    })
    assert response.status_code == 200

    requests.post(url + "/channel/join/v2", json = {
        'token': token1,
        'channel_id': ch_id
    })

    url2 = urlencode({"token": token1, "channel_id": ch_id})

    channel = requests.get(url + 'channel/details/v2?' + url2).json()
    assert u_id not in [user['u_id'] for user in channel['owner_members']] \
            and u_id not in [user['u_id'] for user in channel['all_members']]

#function below needs message_senddm
'''

@clear
def test_removed_user_dm_msg(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2
    u_id = user2.json().get('auth_user_id')
'''