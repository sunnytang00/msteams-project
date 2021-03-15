import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.base.other import clear_v1

channel_blueprint = Blueprint('channel_blueprint', __name__)

@channel_blueprint.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    return dumps({
    })

@channel_blueprint.route("/channel/details/v2", methods=['GET'])
def channel_details():
    return dumps({
    })

@channel_blueprint.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    return dumps({
    })

@channel_blueprint.route("/channel/join/v2", methods=['POST'])
def channel_join():
    return dumps({
    })

@channel_blueprint.route("/channel/addowner/v1", methods=['POST'])
def channel_add_owner():
    return dumps({
    })

@channel_blueprint.route("/channel/removeowner/v1", methods=['POST'])
def channel_remove_owner():
    return dumps({
    })

@channel_blueprint.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    return dumps({
    })