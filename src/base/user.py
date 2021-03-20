from src.base.helper import get_user_data

def user_profile_v1(auth_user_id, u_id):
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
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }