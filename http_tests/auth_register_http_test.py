import requests
from json import loads
from src.config import url
from http_tests.helper import clear

from src.routes.helper import decode_token

@clear
def test_register_basic():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    status_code = response.status_code
    assert status_code == 201

    data = response.json()
    auth_user_id = data.get('auth_user_id')
    assert auth_user_id == 1

    # TODO: when we store UUID we can compare here
    token = data.get('token')
    # expected = decode_token(token)
    # assert uuid == decode_token(token)

    assert token != None