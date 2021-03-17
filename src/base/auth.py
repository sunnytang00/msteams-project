""" Register and login authentication.

This module demonstrates user registration and login authentication as specified by the COMP1531 Major Project specification.
"""

from src.data.data import data
from src.base.error import InputError
from src.base.helper import valid_email, valid_password, valid_first_name, valid_last_name, email_exists, get_handle_str
from json import dump, load
import re

def auth_login_v1(email, password):
    """ Given a registered users' email and password and returns their `auth_user_id` value

    Arguments:
        email (str) - The users email address.
        password (str) - The users password.

    Exceptions:
        InputError - Occurs when email entered is not a valid email as according to project specification.
        InputError - Occurs when the email matches a registered email, but the password is incorrect
        InputError - Occurs when the email entered does not match any registered system

    Return Value:
        Returns auth_user_id (dict) of matching user
    """

    if not valid_email(email):
        raise InputError(f'Email {email} entered is not a valid email')

    for user in data['users']:
        # check user exists
        if email == user['email']:
            # check corret password
            if password == user['password']:
                return {'auth_user_id': user['u_id']}
            else:
                raise InputError(f'Password {password} is not correct')
          
    # email did not match any user
    raise InputError(f'Email {email} entered does not belong to a user')

def auth_register_v1(email, password, name_first, name_last):
    """Register a new user by appending to data

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

    if not valid_email(email):
        raise InputError(f'Email {email} is not a valid email')

    if not valid_password(password):
        raise InputError(f'Password {password} is less than 6 characters long')

    if not valid_first_name(name_first):
        raise InputError(f'name_first {name_first} is not between 1 and 50 characters inclusively in length')

    if not valid_last_name(name_last):
        raise InputError(f'name_last {name_last} is not between 1 and 50 characters inclusively in length')

    if email_exists(email):
        raise InputError(f'Email address {email} is already being used by another user')

    handle_str = get_handle_str(name_first, name_last)

    # register user
    data['users'].append({ 
        'u_id': user_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str,
        'password': password
    })

    return {
        'auth_user_id': user_id,
    }
