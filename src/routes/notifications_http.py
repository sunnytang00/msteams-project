import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.other import clear_v1
from src.notifications import notifactions_get_v1
from src.helper import token_to_auth_user_id

notifications_blueprint = Blueprint('notifications_blueprint', __name__)

@notifications_blueprint.route("/notifications/get/v1", methods=['GET'])
def users_all():
    token = request.args.get('token')

    auth_user_id = token_to_auth_user_id(token)

    notifications = notifactions_get_v1(auth_user_id)

    return dumps({'notifications': notifications}), 200

