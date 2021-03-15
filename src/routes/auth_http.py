import sys
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from src.base.error import InputError
from src.base import config
from src.base.auth import auth_register_v1
from src.base.auth import auth_login_v1

auth_blueprint = Blueprint('auth_blueprint', __name__)
 

@auth_blueprint.route("/auth/register/v2", methods=['POST'])
def register_http():
    
    data = request.get_json()
    

    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']

    auth_user_id = auth_register_v1(email, password, name_first, name_last)

    return dumps({
        #not sure what to do with this'token': token,
        'auth_user_id': auth_user_id,
    }), 200

@auth_blueprint.route("/auth/login/v2", methods=['POST'])
def login_http():
    data = request.get_json()
    email = data['email']
    password = data['password']

    auth_user_id = auth_login_v1(email, password)

    return dumps({
        #'token': token,
        'auth_user_id': auth_user_id
    }), 200