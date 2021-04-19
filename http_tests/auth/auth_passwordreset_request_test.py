import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper

@clear
def test_send_email(helper):
    email = "goergebush2@gmail.com" # sorry goerge for the spam
    helper.register_user(1, email=email)

    response = requests.post(url + 'auth/passwordreset/request/v1', json = {
        'email': email
    })
    assert response.status_code == 200
