from src.http.auth_register_http import register
import requests
from json import loads
from src.base.config import url

def test_register_basic():

    out = requests.post(url + "auth/register/v2", json = {
        'email' : 'harrypotter@gmail.com'
        'password' : 'dumbledore'
        'name_first' : 'harry'
        'name_last' : 'potter'
    })

    output = out.json()

    #may need to assert what token is = to? apparently atm should be user_id
    #but not sure

    assert output['auth_user_id'] == 1