import sys
from json import dumps
from flask import Flask, request, Blueprint

from src.other import clear_v1
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_senddm_v1,\
     message_share_v1, message_react_v1, message_unreact_v1, message_sendlater_v1, message_sendlaterdm_v1, message_pin_v1, message_unpin_v1
from src.helper import token_to_auth_user_id

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
    data = request.get_json()

    token = data.get('token')
    message_id = data.get('message_id')
    message = data.get('message')

    auth_user_id = token_to_auth_user_id(token)
    message_edit_v1(auth_user_id, message_id, message)
    
    return dumps({
    })

@message_blueprint.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    """Given a message_id for a message, this message is removed from the channel/DM

    Arguments:
        token (str)    - unique for each user.
        message_id (int)    - User's message id.
    

    Exceptions:
        InputError  - Occurs when ...
        AccessError - Occurs when ...

    Exceptions:
        InputError - Message (based on ID) no longer exists
        AccessError when none of the following are true:
            - Message with message_id was sent by the authorised user making this request
            - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**
    Return Value:
        Returns empty dict on successfully removing a message.        
    """
    
    
    data = request.get_json()

    token = data.get('token')
    message_id = data.get('message_id')
    auth_user_id = token_to_auth_user_id(token)

    message_remove_v1(auth_user_id, message_id)

    return dumps({
    })



@message_blueprint.route("/message/share/v1", methods=['POST'])
def message_share():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)

    og_message_id = data.get('og_message_id')
    message = data.get('message')
    channel_id = data.get('channel_id')
    dm_id = data.get('dm_id')

    msgs_id = message_share_v1(auth_user_id, og_message_id, message, channel_id, dm_id)

    return dumps({
        'shared_message_id' : msgs_id['shared_message_id']
    }), 200

@message_blueprint.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    dm_id = data.get('dm_id')
    message = data.get('message')

    ret = message_senddm_v1(auth_user_id, int(dm_id), message)
    message_id = ret.get('message_id')

    return dumps({
        'message_id' : message_id
    })
@message_blueprint.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    channel_id = data.get('channel_id')
    message = data.get('message')
    time_sent = data.get('time_sent')

    message_id = message_sendlater_v1(auth_user_id, channel_id, message, time_sent).get('message_id')

    return dumps ({
        'message_id' : message_id
    }), 200

@message_blueprint.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    dm_id = data.get('dm_id')
    message = data.get('message')
    time_sent = data.get('time_sent')

    message_id = message_sendlaterdm_v1(auth_user_id, dm_id, message, time_sent).get('message_id')

    return dumps ({
        'message_id' : message_id
    }), 200

@message_blueprint.route("/message/pin/v1", methods=['POST'])
def message_pin():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    message_id = data.get('message_id')

    message_pin_v1(auth_user_id, message_id)

    return dumps({
    })

@message_blueprint.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)
    message_id = data.get('message_id')

    message_unpin_v1(auth_user_id, message_id)

    return dumps({
    })

"""
@message_blueprint.route("/message/react/v1", methods=['POST'])
def message_react():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)

    message_id = data.get('message_id')
    react_id = data.get('react_id')
    message_react_v1(auth_user_id, message_id, react_id)

    return dumps ({
    })

@message_blueprint.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_auth_user_id(token)

    message_id = data.get('message_id')
    react_id = data.get('react_id')
    message_unreact_v1(auth_user_id, message_id, react_id)

    return dumps ({
    })
"""
