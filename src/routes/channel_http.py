import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.base.channel import channel_details_v1, channel_invite_v1, channel_join_v1, channel_addowner_v1
from src.base.helper import token_to_auth_user_id
from src.base.other import clear_v1

channel_blueprint = Blueprint('channel_blueprint', __name__)

@channel_blueprint.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    token = data.get('token')
    ch_id = data.get('channel_id')
    u_id = data.get('u_id')

    auth_user_id = token_to_auth_user_id(token)

    channel_invite_v1(auth_user_id, ch_id, u_id)

    return dumps({}), 201

@channel_blueprint.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    ch_id = request.args.get('channel_id')
    auth_user_id = token_to_auth_user_id(token)

    channel = channel_details_v1(auth_user_id, int(ch_id))
    return dumps({
        'name': channel.get('name'),
        'is_public': channel.get('is_public'),
        'owner_members': channel.get('owner_members'),
        'all_members': channel.get('all_members')
    }), 200

@channel_blueprint.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    return dumps({
    })

@channel_blueprint.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    token = data.get('token')
    ch_id = data.get('channel_id')

    auth_user_id = token_to_auth_user_id(token)

    channel_join_v1(auth_user_id, ch_id)
    
    return dumps({}), 201

@channel_blueprint.route("/channel/addowner/v1", methods=['POST'])
def channel_add_owner():
    data = request.get_json()
    token = data.get('token')
    ch_id = data.get('channel_id')
    u_id = data.get('u_id')

    auth_user_id = token_to_auth_user_id(token)

    channel_addowner_v1(auth_user_id, ch_id, u_id)

    return dumps({}), 201

@channel_blueprint.route("/channel/removeowner/v1", methods=['POST'])
def channel_remove_owner():
    return dumps({
    })

@channel_blueprint.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    return dumps({
    })