import requests
from json import loads
from src.config import url
from http_tests.helper import clear
import urllib
from src.routes.helper import get_new_session_id, encode_token
@clear

def test_setprofile_basic():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    u_id = 1

    queryString = urllib.parse.urlencode({
        'token' : token,
        'u_id' : u_id
    })
    user = requests.get(url + f'user/profile/v2?{queryString}')

    data = user.json()
    print(data)
    assert data.get('user').get('name_first') == 'harry'
    assert data.get('user').get('name_last') == 'potter'

@clear

def test_input_error():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    queryString = urllib.parse.urlencode({
        'token' : token,
        'u_id' : 2
    })
    user = requests.get(url + f'user/profile/v2?{queryString}')

    assert user.status_code == 400