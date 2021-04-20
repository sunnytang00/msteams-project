import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.helper import token_to_auth_user_id
import urllib
from src.dm import dm_details_v1
from src.helper import token_to_auth_user_id

@clear
def test_basic(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')
    token2 = data2.get('token')

    u_id2 = data2.get('auth_user_id')
    assert u_id2 == 2
    u_id3 = data3.get('auth_user_id')
    assert u_id3 == 3

    dm_info = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })

    readable_dm = dm_info.json()
    dm_id = readable_dm.get('dm_id')

    queryString = urllib.parse.urlencode({
        'token' : token2,
        'dm_id' : dm_id
    })
  
    dm = requests.get(url + f'dm/details/v1?{queryString}')

    assert dm.status_code == 200

    dm_details = dm.json()
    assert dm_details.get('name') == 'cadifinch, harrrrrypottttter, marcoslowery'
    assert dm_details.get('members') == [{'u_id': 1, 
                                        'email': 'harrypotter3@gmail.com', 
                                        'name_first': 'Harrrrry', 
                                        'name_last': 'Pottttter', 
                                        'handle_str': 'harrrrrypottttter', 
                                        'permission_id': 1,
                                        'profile_img_url': ''},
                                        {'u_id': 2, 
                                        'email': 'marcoslowery@gmail.com', 
                                        'name_first': 'Marcos', 
                                        'name_last': 'Lowery', 
                                        'handle_str': 'marcoslowery', 
                                        'permission_id': 2,
                                        'profile_img_url': ''}, 
                                        {'u_id': 3, 
                                        'email': 'cadifinch@gmail.com', 
                                        'name_first': 'Cadi', 
                                        'name_last': 'Finch', 
                                        'handle_str': 'cadifinch', 
                                        'permission_id': 2,
                                        'profile_img_url': ''}]

@clear
def test_input_error(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')
    token2 = data2.get('token')

    u_id2 = data2.get('auth_user_id')
    assert u_id2 == 2
    u_id3 = data3.get('auth_user_id')
    assert u_id3 == 3

    requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })

    queryString = urllib.parse.urlencode({
        'token' : token2,
        'dm_id' : 5
    })
  
    dm = requests.get(url + f'dm/details/v1?{queryString}')

    assert dm.status_code == 400

@clear
def test_access_error(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')
    token3 = data3.get('token')

    u_id2 = data2.get('auth_user_id')
    assert u_id2 == 2
    u_id3 = data3.get('auth_user_id')
    assert u_id3 == 3

    dm_info = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    readable_dm = dm_info.json()
    dm_id = readable_dm.get('dm_id')

    queryString = urllib.parse.urlencode({
        'token' : token3,
        'dm_id' : dm_id
    })
  
    dm = requests.get(url + f'dm/details/v1?{queryString}')

    assert dm.status_code == 403


