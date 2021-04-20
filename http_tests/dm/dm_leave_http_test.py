import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.helper import create_dm_name
import urllib
from src.helper import get_dm
from src.dm import dm_leave_v1
@clear

def test_basic_leave(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')
    token2 = data2.get('token')
    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })

    dm_info = dm.json()
    dm_id = dm_info.get('dm_id')
    assert dm_id == 1
    
    requests.post(url + 'dm/leave/v1', json = {
        'token' : token2,
        'dm_id' : dm_id
    })

    queryString = urllib.parse.urlencode({
        'token' : token,
        'dm_id' : dm_id
    })

    dm1 = requests.get(url + f'dm/details/v1?{queryString}')
    dm_details = dm1.json()

    assert dm_details.get('members') == [{'u_id': 1, 
                                        'email': 'harrypotter3@gmail.com', 
                                        'name_first': 'Harrrrry', 
                                        'name_last': 'Pottttter', 
                                        'handle_str': 'harrrrrypottttter', 
                                        'permission_id': 1,
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
    u_id3 = data3.get('auth_user_id')

    requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })
    
    response = requests.post(url + 'dm/leave/v1', json = {
        'token' : token2,
        'dm_id' : 3
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

    dm = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    dm_info = dm.json()
    dm_id = dm_info.get('dm_id')
    
    response = requests.post(url + 'dm/leave/v1', json = {
        'token' : token3,
        'dm_id' : dm_id
    })

    assert response.status_code == 403


