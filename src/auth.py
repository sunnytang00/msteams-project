""" Register and login authentication.

This module demonstrates user registration and login authentication as specified by the COMP1531 Major Project specification.
"""

from src.error import InputError
from src.helper import valid_email, valid_password, valid_first_name, valid_last_name, email_exists, get_handle_str, get_user_by_email, create_user_stats
from src.data.helper import get_users, store_user, get_user_count, get_owner_count, update_owner_count
import re

def auth_login_v1(email, password):
    """ Given a registered users' email and password and returns their `auth_user_id` value

    Arguments:
        email (str) - The user's email address
        password (str) - The user's password

    Exceptions:
        InputError - Occurs when email entered is not a valid email as according to project specification
        InputError - Occurs when the email matches a registered email, but the password is incorrect
        InputError - Occurs when the email entered does not match any registered system

    Return Value:
        Returns auth_user_id (dict) of matching user
    """

    if not valid_email(email):
        raise InputError(f'Email {email} entered is not a valid email')

    user = get_user_by_email(email)
    
    # email did not match any user.
    if not user:
        raise InputError(f'Email {email} entered does not belong to a user')

    # email matches user.
    if password == user['password']:
        return {'auth_user_id': user['u_id']}
    else:
        raise InputError(f'Password {password} is not correct')    

def auth_register_v1(email, password, name_first, name_last):
    """Register a new user by appending to data

    Arguments:
        email (str) - The user's email address
        password (str) - The user's password
        name_first (str) - The user's first name
        name_last (str) - The user's last name
    
    Exceptions:
        InputError - Occurs when email entered is not a valid email as according to project specification
        InputError - Occurs when email address is already being used by another user
        InputError - Occurs when password entered is less than 6 characters long
        InputError - Occurs when name_first is not between 1 and 50 characters inclusively in length
        InputError - Occurs when name_last is not between 1 and 50 characters inclusively in length

    Return Value:
        Returns dict with auth_user_id on newly created user.
    """
    auth_user_id = get_user_count() + 1

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

    permission_id = 0
    if not get_users(): #if there is no user already registered
        permission_id = 1
        owner_count = get_owner_count() + 1
        update_owner_count(owner_count)
    else:
        permission_id = 2
    user_stats = create_user_stats()
    user = { 
        'u_id': auth_user_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str,
        'password': password,
        'permission_id': permission_id,
        'removed': False,
        'session_list': [],
        'notifications': [],
        'user_stats' : user_stats,
        'reset_code': "",
        'profile_img_url':''
    }

    # register user
    store_user(user)

    return {
        'auth_user_id': auth_user_id,
    }
