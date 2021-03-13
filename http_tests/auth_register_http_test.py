from src.http.auth_register_http import register
import requests
from json import loads
from src.base.config import url

def test_register():
    output = register()
    data = loads(output[0])
    status_code = output[1]

    assert data.get('token') == 'token'
    assert data.get('auth_user_id') == 1
    assert status_code == 201
