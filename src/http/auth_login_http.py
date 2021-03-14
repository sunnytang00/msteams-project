import sys
from json import dumps
from flask import request
from src.base.error import InputError
from src.server import APP
from src.base.config import url
from src.base.auth import auth_login_v1
