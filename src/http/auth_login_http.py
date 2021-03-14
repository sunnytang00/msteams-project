import sys
from json import dumps
from flask import request
from src.base.error import InputError
from src.server import APP
from src.base.config import url
from src.base.auth import auth_login_v1

@APP.route("/auth/login/v2", methods=['POST'])
def login_http1():
    data = request.get_json()
    email = data['email']
    password = data['password']

    auth_user_id = auth_login_v1(email, password)

    return dumps({
        'token': token,
        'auth_user_id': auth_user_id
    }), 200