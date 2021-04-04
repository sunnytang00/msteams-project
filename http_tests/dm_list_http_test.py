import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
import urllib

@clear
def test_basic(helper):
    pass
    """

    response = helper.register_user(1)
    response2 = helper.register_user(2)
    response3 = helper.register_user(3)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()

    token = data.get('token')

    u_id2 = data2.get('auth_user_id')
    assert u_id2 == 2
    u_id3 = data3.get('auth_user_id')
    assert u_id3 == 3

    dm_info = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id2]
    })

    dm_info1 = requests.post(url + 'dm/create/v1', json = {
        'token' : token,
        'u_ids' : [u_id3]
    })

    readable_dm = dm_info.json()
    dm_id = readable_dm.get('dm_id')

    readable_dm1 = dm_info1.json()
    dm_id1 = readable_dm1.get('dm_id')

    queryString = urllib.parse.urlencode({
        'token' : token,
    })
  
    dmlist = requests.get(url + f'dm/list/v1?{queryString}')
    dmlist_info = dmlist.json()
    assert dmlist_info == ['1', '2']
    """