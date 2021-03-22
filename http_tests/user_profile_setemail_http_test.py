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
    auth_user_id = data.get('auth_user_id')
    assert auth_user_id == 1

    requests.put(url + 'user/profile/setemail/v2', json = {
        'auth_user_id' : auth_user_id,
        'email' : 'albusdumbledore@gmail.com',
    })

    u_id = 1

    queryString = urllib.parse.urlencode({
        'auth_user_id' : auth_user_id,
        'u_id' : u_id
    })
    user = requests.get(url + f'user/profile/v2?{queryString}')

    data = user.json()
    assert data.get('user').get('user').get('email') == 'albusdumbledore@gmail.com'
