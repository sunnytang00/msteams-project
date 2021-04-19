import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from src.helper import token_to_auth_user_id

@clear
def test_register_single(helper):
    response = helper.register_user(1)

    assert response.status_code == 201

    data = response.json()
    token = data.get('token')

    auth_user_id = token_to_auth_user_id(token) # if this returns None it means token is invalid

    assert auth_user_id # see if token is valid
    assert auth_user_id == data.get('auth_user_id') # see if returns correct id

@clear
def test_invalid_email(helper):
    """
    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter_is_cool',
        'password' : 'dubledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })
    """
    invalid_email = 'harry_is_cool'
    response = helper.register_user(1, email=invalid_email)

    assert response.status_code == 400

    # data = response.json()
    # data looks like this: {'code': 400, 'name': 'System Error', 'message': '<p>Email harrypotter_is_cool is not a valid email</p>'}
