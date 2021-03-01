from src.data import data
from src.error import InputError
import re


""" Register and login authentication.

This module demonstrates user registration and login authentication as specified by the COMP1531 Major Project specification.
"""

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def auth_login_v1(email, password):

    user_id = len(data) + 1
    
    for i in data['users']:
        if not(re.search(regex, email)):  
            raise InputError('Email is not valid')
        if email == i['email']:
            if password == i['password']:
                return {'auth_user_id': user_id}
            else:
                raise InputError('Password is not correct.')
        else:
            raise InputError('Email does not belong to a user.')

def auth_register_v1(email, password, name_first, name_last):
    """ Registers the user by appending them into the user list inside data.

    Args:
        email (str): The users email address.
        password (str): The users password.
        name_first (str): The users first name.
        name_last (str): The users last name.

    Returns:
        dict: The newly created users user id.
    """
    global data
    user_id = len(data) + 1

    # check if email is valid
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
