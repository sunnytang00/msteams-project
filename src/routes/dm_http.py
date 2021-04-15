import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.other import clear_v1
from src.dm import dm_details_v1, dm_create_v1, dm_list_v1, dm_messages_v1, dm_leave_v1, dm_invite_v1, dm_remove_v1
from src.helper import token_to_auth_user_id
dm_blueprint = Blueprint('dm_blueprint', __name__)

@dm_blueprint.route("/dm/details/v1", methods=['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')

    auth_user_id = token_to_auth_user_id(token)

    details = dm_details_v1(auth_user_id, int(dm_id))
    
    name = details.get('name')
    members = details.get('members')
    return dumps({
        'name' : name,
        'members' : members
    })

@dm_blueprint.route("/dm/list/v1", methods=['GET'])
def dm_list():
    
    token = request.args.get('token')

    auth_user_id = token_to_auth_user_id(token)

    l = dm_list_v1(auth_user_id)
    return dumps({
        'dms' : l
    })

@dm_blueprint.route("/dm/create/v1", methods=['POST'])
def dm_create():
    data = request.get_json()

    token = data.get('token')
    u_ids = data.get('u_ids')
    
    auth_user_id = token_to_auth_user_id(token)

    details = dm_create_v1(auth_user_id, u_ids)
    dm_id = details.get('dm_id')
    dm_name = details.get('dm_name')
    return dumps({
        'dm_id' : dm_id,
        'dm_name' : dm_name
    })

@dm_blueprint.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove(): 

    data = request.get_json()

    token = data.get('token')
    dm_id = data.get('dm_id')

    auth_user_id = token_to_auth_user_id(token)
    dm_remove_v1(auth_user_id, dm_id)
    

    return dumps({
    })

@dm_blueprint.route("/dm/invite/v1", methods=['POST'])
def dm_invite():
    data = request.get_json()

    token = data.get('token')
    dm_id = data.get('dm_id')
    u_id = data.get('u_id')
    
    auth_user_id = token_to_auth_user_id(token)

    dm_invite_v1(auth_user_id, int(dm_id), int(u_id))
    return dumps({
    })

@dm_blueprint.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    data = request.get_json()

    token = data.get('token')
    dm_id = data.get('dm_id')

    auth_user_id = token_to_auth_user_id(token)
    dm_leave_v1(auth_user_id, int(dm_id))

    return dumps({
    })

@dm_blueprint.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')

    auth_user_id = token_to_auth_user_id(token)

    dm_msg = dm_messages_v1(auth_user_id, int(dm_id), int(start))

    messages = dm_msg.get('messages')
    start = dm_msg.get('start')
    end = dm_msg.get('end')

    return dumps({
        'messages' : messages,
        'start' : start,
        'end' : end
    })
