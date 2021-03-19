import requests
from json import loads
from src.config import url
from src.base.other import clear_v1

def test_register_basic():
    requests.delete(url + '/clear/v1', json={})
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    status_code = response.status_code
    assert status_code == 201

    # reading data from response
    data = response.json()
    auth_user_id = data.get('auth_user_id')

    assert auth_user_id == 1
 