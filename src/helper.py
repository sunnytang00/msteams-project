from .data import data
import re

def valid_email(email: str) -> bool:
    """Check if email is valid

    Arguments:
        email (str) - The users email address.

    Return Value:
        Returns bool on regexp evalutaion
    """

    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    return re.search(regex, email)

def user_exists(auth_user_id: int) -> bool:
    for user in data['users']:
        if user['id'] == auth_user_id:
            return True
    return False

def get_user_data(auth_user_id: int) -> dict:
    for user in data['users']:
        if user['id'] == auth_user_id:
            return {
                'email': user['email'],
                'password': user['password'],
                'name_first': user['name_first'],
                'name_last': user['name_last']
            }
    return None