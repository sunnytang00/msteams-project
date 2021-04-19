import sys
from json import dumps
from flask import Flask, request, Blueprint
from src.other import clear_v1

clear_blueprint = Blueprint('clear_blueprint', __name__)

@clear_blueprint.route("/clear/v1", methods=['DELETE'])
def clear():
   clear_v1() 
   return dumps({})