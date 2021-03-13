from src.http.auth_register_http import register
import requests
import json
from src.base.config import url

def test_register():
    register()
    data = {
        'email': 'harrypotter@gmail.com',
        'password': 'jk@3LuSx',
        'name_first': 'Harry',
        'name_last': 'Potter'
        }

    resp = requests.post(url + 'auth/register/v2', json = data)

    print(resp)
    #assert focus_user.get('email') == 'test@example.com'
    assert 2 == 3