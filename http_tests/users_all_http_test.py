import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode

@clear
def test_one_user(helper):
    user1 = helper.register_user(1)
    token1 = user1.json().get('token')
    assert token1

    u_id1 = user1.json().get('auth_user_id')

    url2 = urlencode({"token": token1})

    response = requests.get(url + "users/all/v1?" + url2)
    assert response.status_code == 200
    users = response.json()

    assert u_id1 in [user['u_id'] for user in users['users']]


@clear
def test_multiple_users(helper):
    user1 = helper.register_user(1)
    user2 = helper.register_user(2)
    user3 = helper.register_user(3)
    token1 = user1.json().get('token')
    assert token1

    u_id1 = user1.json().get('auth_user_id')
    u_id2 = user2.json().get('auth_user_id')
    u_id3 = user3.json().get('auth_user_id')
    

    url2 = urlencode({"token": token1})

    response = requests.get(url + "users/all/v1?" + url2)
    assert response.status_code == 200
    users = response.json()

    u_ids = [user['u_id'] for user in users['users']]

    assert u_id1 in u_ids and u_id2 in u_ids and u_id3 in u_ids
