import requests
from json import loads
from src.base.config import url


def test_login_basic_http():
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail1.com',
        'password' : 'dumbledore1',
        'name_first' : 'harry1',
        'name_last' : 'potter1'
    })

    status_code = response.status_code
    # reading data from response
    register_data = response.json()

    login_data = requests.post(url + 'auth/login/v2', json = {
        'email' : 'harrypotter@gmail1.com',
        'password' : 'dumbledore1'
    })

    expected = login_data.json()

    assert register_data == expected
    assert status_code == 200 