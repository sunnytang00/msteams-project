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

    assert dm_details.get('name') == 'cadifinch, marcoslowery'
    
