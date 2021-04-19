import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.helper import create_dm_name
import urllib

@clear

def test_basic(helper):

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')
    u_id2 = data2.get('auth_user_id')
    u_id3 = data3.get('auth_user_id')

    requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id3]
    })

    queryString = urllib.parse.urlencode({
        'token' : token
    })
  
    dm = requests.get(url + f'dm/list/v1?{queryString}')
    dm_info = dm.json()

    assert dm_info.get('dms') == [{'dm_id': 1, 
                                    'name': 'harrrrrypottttter, marcoslowery'},
                                    {'dm_id': 2, 
                                    'name': 'cadifinch, harrrrrypottttter'}]
                                    




