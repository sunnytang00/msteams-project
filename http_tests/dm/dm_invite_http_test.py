import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.helper import create_dm_name
import urllib


@clear
def test_basic_invite(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')

    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    dm_info = dm.json()
    assert dm_info.get('dm_id') == 1

    queryString = urllib.parse.urlencode({
        'token' : token,
        'dm_id' : dm_info.get('dm_id')
    })
  
    dm_deets = requests.get(url + f'dm/details/v1?{queryString}')
    dm_details = dm_deets.json()

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
                                        'profile_img_url': ''}]

    requests.post(url + 'dm/invite/v1', json = {
        'token' : token,
        'dm_id' : dm_info.get('dm_id'),
        'u_id' : u_id3
    })

    queryString = urllib.parse.urlencode({
        'token' : token,
        'dm_id' : dm_info.get('dm_id')
    })
  
    dm_deets = requests.get(url + f'dm/details/v1?{queryString}')
    dm_details = dm_deets.json()

    assert dm_details.get('name') == 'harrrrrypottttter, marcoslowery'
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

    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    dm_info = dm.json()
    assert dm_info.get('dm_id') == 1

    queryString = urllib.parse.urlencode({
        'token' : token,
        'dm_id' : dm_info.get('dm_id')
    })
  
    dm_deets = requests.get(url + f'dm/details/v1?{queryString}')
    dm_details = dm_deets.json()

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
                                        'profile_img_url': ''}]

    response = requests.post(url + 'dm/invite/v1', json = {
        'token' : token,
        'dm_id' : 5,
        'u_id' : u_id3
    })

    assert response.status_code == 400

@clear
def test_input_error2(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)

    data = response.json()
    data2 = response2.json()

    token = data.get('token')

    u_id2 = data2.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    dm_info = dm.json()
    assert dm_info.get('dm_id') == 1

    queryString = urllib.parse.urlencode({
        'token' : token,
        'dm_id' : dm_info.get('dm_id')
    })
  
    dm_deets = requests.get(url + f'dm/details/v1?{queryString}')
    dm_details = dm_deets.json()

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
                                        'profile_img_url': ''}]

    response = requests.post(url + 'dm/invite/v1', json = {
        'token' : token,
        'dm_id' : dm_info.get('dm_id'),
        'u_id' : 5
    })

    assert response.status_code == 400

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
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    dm_info = dm.json()
    assert dm_info.get('dm_id') == 1

    queryString = urllib.parse.urlencode({
        'token' : token,
        'dm_id' : dm_info.get('dm_id')
    })
  
    dm_deets = requests.get(url + f'dm/details/v1?{queryString}')
    dm_details = dm_deets.json()

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
                                        'profile_img_url': ''}]

    response = requests.post(url + 'dm/invite/v1', json = {
        'token' : token3,
        'dm_id' : dm_info.get('dm_id'),
        'u_id' : u_id3
    })

    assert response.status_code == 403


