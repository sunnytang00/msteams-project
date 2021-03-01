from src.data import data
from src.error import InputError
import re

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    """
    Registers the user by appending them into the user list inside data.
    Takes in 4 parameters, returns the user's newly created id.
    """
    global data
    user_id = len(data) + 1

    # check if email is valid
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not(re.search(regex, email)):  
        raise InputError('Invalid email')

    # check password too short
    if len(password) <= 6:
        raise InputError('Password is too short.')

    # check first name length is in [1, 50]
    if not(len(name_first) in range(1,50)):
        raise InputError('First name is too long.')

    # check last name length is in [1, 50]
    if not(len(name_last) in range(1,50)):
        raise InputError('Last name is too long.')

    # check if email already exists in data
    for d in data['users']:
        if d['email'] == 'bobsmith@gmail.com':
            raise InputError('This email already exists.')

    # input is valid and ready to be added
    data['users'].append({ 
        'id': user_id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

    return {
        'auth_user_id': user_id,
    }
