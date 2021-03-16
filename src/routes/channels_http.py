import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.base.other import clear_v1
from src.base.channels import channels_create_v1
channels_blueprint = Blueprint('channels_blueprint', __name__)

@channels_blueprint.route("/channels/list/v2", methods=['GET'])
def channels_list():
    return dumps({
    })

@channels_blueprint.route("/channels/listall/v2", methods=['GET'])
def channels_list_all():
    return dumps({
    })

@channels_blueprint.route("/channels/create/v2", methods=['POST'])
def channels_create():
    data = request.get_json()
    auth_user_id = data.get('auth_user_id')
    name = data.get('name')
    is_public = data.get('is_public')
    
    channel = channels_create_v1(auth_user_id, name, is_public)
    channel_id = channel.get('channel_id')

    return dumps({
        'channel_id' : channel_id
    }), 201