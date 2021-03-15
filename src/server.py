import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.base.error import InputError
from src.base import config
from src.base.auth import auth_register_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


@APP.route("/auth/register/v2", methods=['POST'])
def register():
    
    data = request.get_json()
    
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    

    auth_user_id = auth_register_v1(email, password, name_first, name_last)

    return dumps({
        #not sure what to do with this'token': token,
        'auth_user_id': auth_user_id,
    })

"""
@APP.route("/auth/login/v2", methods=['POST'])
def login_http():
    data = request.get_json()
    email = data['email']
    password = data['password']

    auth_user_id = auth_login_v1(email, password)

    return dumps({
        'token': token,
        'auth_user_id': auth_user_id
    }), 200

"""

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
