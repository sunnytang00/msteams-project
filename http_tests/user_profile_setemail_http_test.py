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
    assert data.get('user').get('user').get('email') == 'albusdumbledore@gmail.com'
