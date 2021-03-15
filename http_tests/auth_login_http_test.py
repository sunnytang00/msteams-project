#from src.server import login
from src.server import register
import requests
from json import loads
from src.base.config import url


def test_login_basic_http():
    """

    out = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    output = register_http()
    out1 = output.json()

    r = requests.post(url + 'auth/login/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore'
    })

    r1 = login_http()
    r_output = r1.json()

    assert r_output['auth_user_id'] == out1['auth_user_id']
    """
    pass