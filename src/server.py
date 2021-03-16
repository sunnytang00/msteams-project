import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.base.error import InputError
from src.base import config
from src.base.auth import auth_register_v1
from src.base.auth import auth_login_v1
from src.base.channels import channels_create_v1

from src.routes.auth_http import auth_blueprint
from src.routes.clear_http import clear_blueprint
from src.routes.channels_http import channels_blueprint
from src.routes.channel_http import channel_blueprint

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
### Register routes ###
APP.register_blueprint(auth_blueprint)
APP.register_blueprint(clear_blueprint)
APP.register_blueprint(channels_blueprint)
APP.register_blueprint(channel_blueprint)
#######################
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


#TODO ALL OF THE BELOW FUNCTIONS (use blueprints)
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

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
