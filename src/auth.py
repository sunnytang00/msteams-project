from src.data import data
from src.error import InputError
from src.helper import valid_email
import re

""" Register and login authentication.

This module demonstrates user registration and login authentication as specified by the COMP1531 Major Project specification.
"""

regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'

def auth_login_v1(email, password):
    """ TODO: add docstring
    """

    user_id = len(data['users']) + 1
    
    for user in data['users']:
        if not(re.search(regex, email)):  
            raise InputError('Email is not valid')
        if email == user['email']:
            if password == user['password']:
                return {'auth_user_id': user_id}
            else:
                raise InputError('Password is not correct.')
        else:
            raise InputError('Email does not belong to a user.')

def auth_register_v1(email, password, name_first, name_last):
    """ Given a user's first and last name, email address, and password, create a new account by appending to data.

    Arguments:
        email (str) - The users email address.
        password (str) - The users password.
        name_first (str) - The users first name.
        name_last (str) - The users last name.
    
    Exceptions:
        InputError - Occurs when email entered is not a valid email as according to project specification.
        InputError - Occurs when email address is already being used by another user.
        InputError - Occurs when password entered is less than 6 characters long.
        InputError - Occurs when name_first is not between 1 and 50 characters inclusively in length.
        InputError - Occurs when name_last is not between 1 and 50 characters inclusively in length.

    Return Value:
        Returns auth_user_id (dict) on newly created user.
    """
    global data
    user_id = len(data['users']) + 1

    # check if email is valid
    if not valid_email(email):
        raise InputError('Invalid email')

    # check password too short
    if len(password) <= 6:
        raise InputError('Password is too short.')

    # check first name length is in [1, 50]
    if not(len(name_first) in range(1,50)):
        raise InputError('First name invalid length.')

    # check last name length is in [1, 50]
    if not(len(name_last) in range(1,50)):
        raise InputError('Last name invalid length.')

    # check if email already exists in data
    for user in data['users']:
        if user['email'] == email:
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
