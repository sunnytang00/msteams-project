import requests
from json import loads
from src.config import url
from http_tests.helper import clear
import urllib
@clear

def test_setname_basic():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    requests.put(url + 'user/profile/setname/v2', json = {
        'token' : token,
        'name_first' : 'albus',
        'name_last' : 'dumbledore'
    })

    u_id = 1

    queryString = urllib.parse.urlencode({
        'token' : token,
        'u_id' : u_id
    })
    user = requests.get(url + f'user/profile/v2?{queryString}')

    data = user.json()
    assert data.get('user').get('name_first') == 'albus'
    assert data.get('user').get('name_last') == 'dumbledore'

@clear

def test_inputerror1():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    response = requests.put(url + 'user/profile/setname/v2', json = {
        'token' : token,
        'name_first' : 'a' * 51,
        'name_last' : 'dumbledore'
    })

    assert response.status_code == 400

@clear

def test_inputerror2():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    response = requests.put(url + 'user/profile/setname/v2', json = {
        'token' : token,
        'name_first' : 'albus',
        'name_last' : 'd' * 51
    })

    assert response.status_code == 400