"""TODO"""
from src.base.helper import get_user_data
from src.base.helper import valid_email, valid_password, valid_first_name, valid_last_name, email_exists, get_handle_str, handle_str_exists
from src.base.error import InputError
from src.data.helper import get_users, update_name_first, update_name_last, update_email, update_handle_str 

def user_profile_v1(auth_user_id, u_id):
    """TODO"""
    # TODO: add valid user checking
    user = get_user_data(u_id)

    email = user.get('email')
    name_first = user.get('name_first')
    name_last = user.get('name_last')
    handle_str = user.get('handle_str')

    return {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': handle_str,
        },
    }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    """TODO"""

    if not valid_first_name(name_first):
        raise InputError(f'name_first {name_first} is not between 1 and 50 characters inclusively in length')

    if not valid_last_name(name_last):
        raise InputError(f'name_last {name_last} is not between 1 and 50 characters inclusively in length')
        
    for user in get_users():
        if user['u_id'] == auth_user_id:
            update_name_first(auth_user_id, name_first)
            update_name_last(auth_user_id, name_last)
    return {}

def user_profile_setemail_v1(auth_user_id, email):
    """TODO"""

    if not valid_email(email):
        raise InputError(f'Email {email} is not a valid email')

    if email_exists(email):
        raise InputError(f'Email address {email} is already being used by another user') 
        
    for user in get_users():
        if user['u_id'] == auth_user_id:
            update_email(auth_user_id, email)

    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    """TODO"""

    #need to change to tokens eventually
    if len(handle_str) not in range(3, 21):
        raise InputError(f'Handle string {handle_str} is not between 3 and 20 characters inclusive')

    if handle_str_exists(handle_str):
        raise InputError(f'Handle string {handle_str} is already in use')

    for user in get_users():
        if user['u_id'] == auth_user_id:
            update_handle_str(auth_user_id, handle_str)

    return {
    }
