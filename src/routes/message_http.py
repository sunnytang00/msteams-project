import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.base.other import clear_v1
from src.base.message import message_send_v1, message_remove_v1, message_edit_v1, message_senddm_v1
from src.base.helper import token_to_auth_user_id
message_blueprint = Blueprint('message_blueprint', __name__)

@message_blueprint.route("/message/send/v2", methods=['POST'])
def message_send():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    channel_id = data.get('channel_id')
    message = data.get('message')

    ret = message_send_v1(auth_user_id, channel_id, message)
    message_id = ret.get('message_id')
    return dumps({
        'message_id' : message_id
    })


@message_blueprint.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    """
    data = request.get_json()

    auth_user_id = data.get('auth_user_id')
    message_id = data.get('message_id')
    message = data.get('message')

    message_edit_v1(auth_user_id, message_id, message)
    """
    return dumps({
    })

@message_blueprint.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    return dumps({
    })


@message_blueprint.route("/message/share/v1", methods=['POST'])
def message_share():
    return dumps({
    })

@message_blueprint.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    return dumps({
    })