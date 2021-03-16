import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.base.other import clear_v1

channels_blueprint = Blueprint('channels_blueprint', __name__)

@channels_blueprint.route("/channels/list/v2", methods=['GET'])
def channel_list():
    return dumps({
    })

@channels_blueprint.route("/channels/listall/v2", methods=['GET'])
def channel_list_all():
    return dumps({
    })

@channels_blueprint.route("/channels/create/v2", methods=['POST'])
def channel_create():
    
    return dumps({
    })