import requests
from json import loads
from src.base.config import url


def test_login_basic_http():
    
    r = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail1.com',
        'password' : 'dumbledore1',
        'name_first' : 'harry1',
        'name_last' : 'potter1'
    })

    output = r.json()

    out = requests.post(url + 'auth/login/v2', json = {
        'email' : 'harrypotter@gmail1.com',
        'password' : 'dumbledore1'
    })

    expected = out.json()

    assert output['auth_user_id'] == expected['auth_user_id']
    
    
    