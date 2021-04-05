import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.routes.notifications_http import notifactions_get_v1
from urllib.parse import urlencode

@clear
def test_invite_user_into_channel(helper):
    user1 = helper.register_user(1, name_first='bob', name_last='smith')
    user2 = helper.register_user(2)
    
    token1 = user1.json().get('token')
    token2 = user2.json().get('token')
    assert token1 and token2

    u_id = user2.json().get('auth_user_id')

    ch_id = helper.create_channel(1,token1, 'Harvey N', True).json().get('channel_id')

    requests.post(url + "/channel/invite/v2", json = {
        'token': token1,
        'channel_id' : ch_id,
        'u_id': u_id
    })

    url2 = urlencode({"token": token2})

    response = requests.get(url + "notifications/get/v1?" + url2)
    assert response.status_code == 200

    notifications = response.json().get('notifications')
    print(response.json())
    assert len(notifications) == 1
    assert notifications[0].get('notification_message') == 'bobsmith added you to Harvey N'

@clear
def test_empty_notifications(helper):
    user1 = helper.register_user(1, name_first='bob', name_last='smith')
    token1 = user1.json().get('token')

    url2 = urlencode({"token": token1})
    response = requests.get(url + "notifications/get/v1?" + url2)
    print(response.json())
    assert response.status_code == 200
