import requests
from json import loads
from src.base.config import url
from src.server import register

def test_register_basic():
    
    r = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    output = r.json()

    #may need to assert what token is = to? apparently atm should be user_id
    #but not sure

    assert output['auth_user_id'] == {'auth_user_id' : 1}
 