"""TODO"""
from src.helper import get_user
from src.helper import valid_email, valid_password, valid_first_name, valid_last_name, email_exists, \
                            get_handle_str, handle_str_exists, get_current_user
from src.error import InputError
from src.data.helper import get_users, update_name_first, update_name_last, update_email, update_handle_str 

def user_profile_v1(auth_user_id, u_id):
    """For a valid user, 
    returns information about their user_id, email, first name, last name, and handle

    Args:
        auth_user_id (int): id of authenticated user
        u_id (int): id of user profile to be looked at

    Raises:
        InputError: User with u_id is not a valid user

    Returns:
        A dict user, which contains u_id, email, first and last name, and handle string
    """    """TODO"""
    user = get_user(u_id)
    if not bool(user):
        raise InputError(f'User with u_id {u_id} is not a valid user')

    email = user.get('email')
    name_first = user.get('name_first')
    name_last = user.get('name_last')
    handle_str = user.get('handle_str')

    if not get_current_user(u_id):
        name_first = 'Removed'
        name_last = 'user'

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
    """Update the authorised user's first and last name

    Args:
        auth_user_id (int): id of user to change name
        name_first (str): new first name
        name_last (str):  new last name

    Raises:
        InputError: name_first is not between 1 and 50 characters inclusively in length
        InputError: name_last is not between 1 and 50 characters inclusively in length
    """ 

    if not valid_first_name(name_first):
        raise InputError(f'name_first {name_first} is not between 1 and 50 characters inclusively in length')

    if not valid_last_name(name_last):
        raise InputError(f'name_last {name_last} is not between 1 and 50 characters inclusively in length')

    # TODO: repalce with helper    
    for user in get_users():
        if user['u_id'] == auth_user_id:
            update_name_first(auth_user_id, name_first)
            update_name_last(auth_user_id, name_last)
    return {}

def user_profile_setemail_v1(auth_user_id, email):
    """Update the authorised user's email address

    Args:
        auth_user_id (int): id of user to change email
        email (str): new email

    Raises:
        InputError: Email entered is not a valid email
        InputError: Email address is already being used by another user
    """ 

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
    """Update the authorised user's handle (i.e. display name)

    Args:
        auth_user_id (int): id of user to change handle
        handle_str (str): new display name

    Raises:
        InputError: handle_str is not between 3 and 20 characters inclusive
        InputError: handle is already used by another user
    """    
    if len(handle_str) not in range(3, 21):
        raise InputError(f'Handle string {handle_str} is not between 3 and 20 characters inclusive')

    if handle_str_exists(handle_str):
        raise InputError(f'Handle string {handle_str} is already in use')

    for user in get_users():
        if user['u_id'] == auth_user_id:
            update_handle_str(auth_user_id, handle_str)

    return {
    }
