import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.other import clear_v1
from src.standup import standup_start_v1, standup_send_v1, standup_active_v1
from src.helper import token_to_auth_user_id

standup_blueprint = Blueprint('standup_blueprint', __name__)

@standup_blueprint.route("/standup/start/v1", methods=['POST'])
def standup_start():
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')
    length = data.get('length')

    auth_user_id = token_to_auth_user_id(token)

    time_finish = standup_start_v1(auth_user_id, channel_id, length).get('time_finish')

    return dumps({
        'time_finish': time_finish
    }), 200

@standup_blueprint.route("/standup/active/v1", methods=['GET'])
def standup_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    auth_user_id = token_to_auth_user_id(token)

    standup_data = standup_active_v1(auth_user_id, int(channel_id))

    return dumps({
        'is_active': standup_data.get('is_active'),
        'time_finish': standup_data.get('time_finish')
    }), 200

@standup_blueprint.route("/standup/send/v1", methods=['POST'])
def standup_send():
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')
    message = data.get('message')
    
    auth_user_id = token_to_auth_user_id(token)

    standup_send_v1(auth_user_id, channel_id, message)

    return dumps({}), 200
