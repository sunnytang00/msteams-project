import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.base.helper import token_to_auth_user_id
import urllib
from src.base.dm import dm_details_v1
from src.base.helper import token_to_auth_user_id
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
    u_id3 = data3.get('auth_user_id')

    dm_info = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2, u_id3]
    })

    readable_dm = dm_info.json()
    dm_id = readable_dm.get('dm_id')
    print(dm_id)

    details = dm_details_v1(2,dm_id)
    name = details.get('name')
    members = details.get('members')
    print(name)
    print(members)
    print(token_to_auth_user_id(token2))
    queryString = urllib.parse.urlencode({
        'token' : token2,
        'dm_id' : dm_id
    })
  
    dm = requests.get(url + f'dm/details/v1?{queryString}')
    dm_details = dm.json()
    print(dm)
    print(dm_details)
    print(dm_details.get('name'))
    print(dm_details.get('members'))
    assert dm_details.get('name') == 'cadifinch, marcoslowery'
    
