import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.base.error import InputError
from src.base import config
from src.base.auth import auth_register_v1
from src.base.auth import auth_login_v1

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
    }), 200


@APP.route("/auth/login/v2", methods=['POST'])
def login_http():
    data = request.get_json()
    email = data['email']
    password = data['password']

    auth_user_id = auth_login_v1(email, password)

    return dumps({
        #'token': token,
        'auth_user_id': auth_user_id
    }), 200

#TODO ALL OF THE BELOW FUNCTIONS
@APP.route("/auth/logout/v1", methods=['POST'])
def logout():
    return dumps({
    })

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    return dumps({
    })

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    return dumps({
    })

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    return dumps({
    })

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    return dumps({
    })

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_add_owner():
    return dumps({
    })

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_remove_owner():
    return dumps({
    })

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    return dumps({
    })

@APP.route("/channels/list/v2", methods=['GET'])
def channel_list():
    return dumps({
    })

@APP.route("/channels/listall/v2", methods=['GET'])
def channel_list_all():
    return dumps({
    })

@APP.route("/channels/create/v2", methods=['POST'])
def channel_create():
    return dumps({
    })

@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    return dumps({
    })

@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    return dumps({
    })

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    return dumps({
    })

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    return dumps({
    })

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    return dumps({
    })

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    return dumps({
    })


@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    return dumps({
    })

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    return dumps({
    })

@APP.route("/dm/invite/v1", methods=['POST'])
def dm_invite():
    return dumps({
    })

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    return dumps({
    })

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    return dumps({
    })

@APP.route("/message/senddm/v1", methods=['POST'])
def message_send_dm():
    return dumps({
    })

@APP.route("/user/profile/v2", methods=['GET'])
def user_profile():
    return dumps({
    })

@APP.route("/user/profile/setname/v2", methods=['PUT'])
def user_profile_set_name():
    return dumps({
    })

@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def user_profile_set_email():
    return dumps({
    })

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_set_handle():
    return dumps({
    })

@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    return dumps({
    })

@APP.route("/search/v2", methods=['GET'])
def search():
    return dumps({
    })

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    return dumps({
    })

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_user_permission_change():
    return dumps({
    })

@APP.route("/notifications/get/v1", methods=['GET'])
def notification_get():
    return dumps({
    })

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    return dumps({
    })



if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
