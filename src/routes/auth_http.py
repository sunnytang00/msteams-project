import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.base.auth import auth_register_v1
from src.base.auth import auth_login_v1

from src.routes.helper import sha256_hash, get_new_session_id, encode_token
from src.data.helper import store_session_id

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route("/auth/register/v2", methods=['POST'])
def register_http():
    
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    hashed_password = sha256_hash(password)
    name_first = data.get('name_first')
    name_last = data.get('name_last')

    user = auth_register_v1(email, hashed_password, name_first, name_last)
    auth_user_id = user.get('auth_user_id')

    new_session_id = get_new_session_id() # i.e. uuid
    store_session_id(auth_user_id, new_session_id) 

    token = encode_token(new_session_id)

    return dumps({
        'token': token,
        'auth_user_id': auth_user_id
    }), 201

@auth_blueprint.route("/auth/login/v2", methods=['POST'])
def login_http():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    hashed_password = sha256_hash(password)

    user = auth_login_v1(email, hashed_password)
    auth_user_id = user.get('auth_user_id')

    return dumps({
        #'token': token,
        'auth_user_id': auth_user_id
    }), 200

@auth_blueprint.route("/auth/logout/v1", methods=['POST'])
def logout():
    return dumps({
    })