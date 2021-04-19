import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.other import clear_v1
from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.helper import token_to_auth_user_id
channels_blueprint = Blueprint('channels_blueprint', __name__)

@channels_blueprint.route("/channels/list/v2", methods=['GET'])
def channels_list():
    token = request.args.get('token')
    auth_user_id = token_to_auth_user_id(token)
    channels = channels_list_v1(auth_user_id)
    return dumps({
        'channels': channels['channels']
    }), 200

@channels_blueprint.route("/channels/listall/v2", methods=['GET'])
def channels_list_all():
    token = request.args.get('token')
    auth_user_id = token_to_auth_user_id(token)
    channels = channels_listall_v1(auth_user_id)
    return dumps({
        'channels': channels['channels']
    }), 200

@channels_blueprint.route("/channels/create/v2", methods=['POST'])
def channels_create():
    data = request.get_json()
    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    name = data.get('name')
    is_public = data.get('is_public')
    
    channel = channels_create_v1(auth_user_id, name, is_public)
    channel_id = channel.get('channel_id')

    return dumps({
        'channel_id' : channel_id
    }), 200