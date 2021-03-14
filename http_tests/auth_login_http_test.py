from src.http.auth_login_http import login
import requests
from json import loads
from src.base.config import url


def test_login_basic():

    out = requests.post(url + "auth/register/v2", json = {
        'email' : 'harrypotter@gmail.com'
        'password' : 'dumbledore'
        'name_first' : 'harry'
        'name_last' : 'potter'
    })

    output = out.json()

    r = requests.post(url + "auth/login/v2", json = {
        'email' : 'harrypotter@gmail.com   '
        'password' : 'dumbledore'

    })

    r_output = r.json()

    assert r_output['auth_user_id'] == output['auth_user_id']
    