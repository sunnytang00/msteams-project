import requests
from json import loads
from src.config import url
from http_tests.helper import clear
import urllib
@clear

def test_sethandle_basic():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    requests.put(url + 'user/profile/sethandle/v1', json = {
        'token' : token,
        'handle_str' : 'teststring',
    })

    u_id = 1

    queryString = urllib.parse.urlencode({
        'token' : token,
        'u_id' : u_id
    })
    user = requests.get(url + f'user/profile/v2?{queryString}')

    data = user.json()
    assert data.get('user').get('handle_str') == 'teststring'

@clear

def test_tooshort():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    error = requests.put(url + 'user/profile/sethandle/v1', json = {
        'token' : token,
        'handle_str' : '22',
    })

    assert error.status_code == 400

@clear

def test_inuse():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter1@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'james',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    error = requests.put(url + 'user/profile/sethandle/v1', json = {
        'token' : token,
        'handle_str' : 'jamespotter',
    })

    assert error.status_code == 400


