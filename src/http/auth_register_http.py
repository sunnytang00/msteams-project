import sys
from json import dumps
from flask import request
from src.base.error import InputError
from src.server import APP
from src.base.config import url
from src.base.auth import auth_register_v1

@APP.route("/auth/register/v2", methods=['POST'])
def register():
    token = 'token'

    email = 'harrypotter@gmail.com'
    password = 'ka#sDlj9xc'
    name_first = 'Harry'
    name_last = 'Harry'

    user = auth_register_v1(email, password, name_first, name_last)
    auth_user_id = user.get('auth_user_id')

    return dumps({
        'token': token,
        'auth_user_id': auth_user_id
    }), 201