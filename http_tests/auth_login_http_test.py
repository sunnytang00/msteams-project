import requests
from json import loads
from src.config import url
from http_tests.helper import clear

# TODO: BROKEN TEST... Come back to later when finished iter-1 work...
"""
@clear
def test_login_basic_http():
    ### register
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail1.com',
        'password' : 'dumbledore1',
        'name_first' : 'harry1',
        'name_last' : 'potter1'
    })

    status_code = response.status_code
    assert status_code == 201

    register_data = response.json()
    registered_auth_user_id = register_data.get('auth_user_id')

    ### login user
    response = requests.post(url + 'auth/login/v2', json = {
        'email' : 'harrypotter@gmail1.com',
        'password' : 'dumbledore1'
    })
    status_code = response.status_code
    assert status_code == 200 

    login_data = response.json()
    expected_auth_user_id = login_data.get('auth_user_id')

    assert registered_auth_user_id == expected_auth_user_id
"""