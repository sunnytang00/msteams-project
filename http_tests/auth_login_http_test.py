#from src.server import login
from src.server import register
import requests
from json import loads
from src.base.config import url


def test_login_basic_http():

    r = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    output = r.json()

    out = requests.post(url + 'auth/login/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore'
    })

    expected = out.json()

    assert output['auth_user_id'] == expected['auth_user_id']
    