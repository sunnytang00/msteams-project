import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper

@clear
def test_login_basic_http(helper):
    ### register
    response = helper.register_user(value=1, email='harrypotter@gmail1.com', password='dumbledore1')

    status_code = response.status_code
    assert status_code == 200

    register_data = response.json()
    registered_auth_user_id = register_data.get('auth_user_id')
    register_token = register_data.get('token')

    ### login user
    response = requests.post(url + 'auth/login/v2', json = {
        'email' : 'harrypotter@gmail1.com',
        'password' : 'dumbledore1'
    })
    status_code = response.status_code
    assert status_code == 200 

    login_data = response.json()
    expected_auth_user_id = login_data.get('auth_user_id')
    expected_token = login_data.get('token')

    assert registered_auth_user_id == expected_auth_user_id
    assert expected_token != register_token #to show a new token has been generated