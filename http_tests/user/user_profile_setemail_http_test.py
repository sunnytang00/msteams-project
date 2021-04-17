import requests
from json import loads
from src.config import url
from http_tests.helper import clear
import urllib
@clear

def test_setemail_basic():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    token = data.get('token')

    requests.put(url + 'user/profile/setemail/v2', json = {
        'token' : token,
        'email' : 'albusdumbledore@gmail.com',
    })

    u_id = 1

    queryString = urllib.parse.urlencode({
        'token' : token,
        'u_id' : u_id
    })
    user = requests.get(url + f'user/profile/v2?{queryString}')

    data = user.json()
    assert data.get('user').get('email') == 'albusdumbledore@gmail.com'

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

    response = requests.put(url + 'user/profile/setemail/v2', json = {
        'token' : token,
        'email' : 'invalidemail!!!!!!!!',
    })

    assert response.status_code == 400

@clear

def test_input_error2():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    data = response.json()
    u_id = data.get('auth_user_id')

    response2 = requests.post(url + 'auth/register/v2', json = {
        'email' : 'jamespotter@gmail.com',
        'password' : 'severussnape',
        'name_first' : 'james',
        'name_last' : 'potter'
    })
    data2 = response2.json()
    token2 = data2.get('token')
    token = data.get('token')

    
    queryString = urllib.parse.urlencode({
        'token' : token,
        'u_id' : u_id
    })
    user = requests.get(url + f'user/profile/v2?{queryString}')
    data = user.json()
    email = data.get('user').get('email')


    response = requests.put(url + 'user/profile/setemail/v2', json = {
        'token' : token2,
        'email' : email,
    })

    assert response.status_code == 400

