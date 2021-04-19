import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper

@clear
def test_send_email(helper):
    email = "georgebush2@gmail.com" # sorry george for the spam
    helper.register_user(1, email=email)

    response = requests.post(url + 'auth/passwordreset/request/v1', json = {
        'email': email
    })
    assert response.status_code == 200

@clear
def test_full_passwordreset(helper):
    email = "georgebush2@gmail.com" # sorry george for the spam x2
    helper.register_user(1, email=email)

    response = requests.post(url + 'auth/passwordreset/request/v1', json = {
        'email': email
    })
    assert response.status_code == 200