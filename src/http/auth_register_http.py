import sys
from json import dumps
from flask import request
from src.base.error import InputError
from src.server import APP
from src.base.config import url
from src.base.auth import auth_register_v1

@APP.route("/auth/register/v2", methods=['POST'])
def register_http1():
    
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    """
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    """

    auth_user_id = auth_register_v1(email, password, name_first, name_last)

    return dumps({
        'auth_user_id': auth_user_id
        'token': token,
    }), 200
