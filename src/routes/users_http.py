import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.other import clear_v1
from src.users import users_all_v1
from src.helper import token_to_auth_user_id

users_blueprint = Blueprint('users_blueprint', __name__)

@users_blueprint.route("/users/all/v1", methods=['GET'])
def users_all():
    token = request.args.get('token')

    auth_user_id = token_to_auth_user_id(token)

    users = users_all_v1(auth_user_id)

    return dumps({'users': users}), 200