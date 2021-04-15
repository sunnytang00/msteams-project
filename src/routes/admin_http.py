import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.other import clear_v1
from src.admin import admin_userpermission_change_v1, admin_user_remove_v1
from src.helper import token_to_auth_user_id

admin_blueprint = Blueprint('admin_blueprint', __name__)

@admin_blueprint.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change():
    data = request.get_json()
    token = data.get('token')
    u_id = data.get('u_id')
    permission_id = data.get('permission_id')

    auth_user_id = token_to_auth_user_id(token)
    admin_userpermission_change_v1(auth_user_id, u_id, permission_id)

    return dumps({}), 200

@admin_blueprint.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    data = request.get_json()
    token = data.get('token')
    u_id = data.get('u_id')

    auth_user_id = token_to_auth_user_id(token)
    admin_user_remove_v1(auth_user_id, u_id)

    return dumps({}), 200