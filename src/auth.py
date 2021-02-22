from src.data import data
from src.error import InputError
import re

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    global data
    user_id = len(data) + 1

    # validate email
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    # if the email is not correct
    if not(re.search(regex, email)):  
        raise InputError('Invalid email')

    # input is valid and ready to be added
    data['users'] = {
        'id': user_id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    }
    return {
        'auth_user_id': user_id,
    }
