import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_setname_v1, \
                    user_profile_sethandle_v1, user_stats_v1, user_profile_uploadphoto_v1
from src.helper import token_to_auth_user_id

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route("/user/profile/v2", methods=['GET'])
def user_profile():
    #token
    token = request.args.get('token')

    auth_user_id = token_to_auth_user_id(token)
    u_id = request.args.get('u_id')

    user = user_profile_v1(auth_user_id, int(u_id))

    return dumps({
        'user': user.get('user')
    })

@user_blueprint.route("/user/profile/setname/v2", methods=['PUT'])
def user_profile_setname():

    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    name_first = data.get('name_first')
    name_last = data.get('name_last')

    #need to change to token
    user_profile_setname_v1(auth_user_id, name_first, name_last)

    return dumps({
    })


#NEED TO CHANGE TO TOKEN

@user_blueprint.route("/user/profile/setemail/v2", methods=['PUT'])
def user_profile_setemail():

    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    email = data.get('email')

    user_profile_setemail_v1(auth_user_id, email)
    
    return dumps({
    })

@user_blueprint.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():

    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    handle_str = data.get('handle_str')

    user_profile_sethandle_v1(auth_user_id, handle_str)
    
    return dumps({
    })

@user_blueprint.route("/user/stats/v1", methods=['GET'])
def user_stats():
    token = request.args.get('token')
    auth_user_id = token_to_auth_user_id(token)
    
    user_stats = user_stats_v1(auth_user_id)
    
    return dumps({
        'user_stats' : user_stats
    })

@user_blueprint.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_profile_uploadphoto():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    img_url = data.get('img_url')
    x_start = data.get('x_start')
    y_start = data.get('y_start')
    x_end = data.get('x_end')
    y_end = data.get('y_end')

    user_profile_uploadphoto_v1(auth_user_id, img_url, x_start, y_start, x_end, y_end)
    return dumps({}), 200