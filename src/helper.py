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

def channel_exists(channel_id: int) -> bool:
    for channel in data['channels']:
        if channel['id'] == channel_id:
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

def get_channel_data(channel_id: int) -> bool:
    for channel in data['channels']:
        if channel['id'] == channel_id:
            return {
                'id': channel['id'],
                'name': channel['name'],
                'user_id': channel['user_id'],
                'owner_members': channel['owner_members'],
                'all_members' : channel['all_members'],
                'messages' : channel['messages'],
                'is_public' : channel['is_public']
            }
    return None

def user_is_member(channel: dict, auth_user_id: int) -> bool:
    for members in channel['all_members']:
        print(members)
        if members['u_id'] == auth_user_id:
            return True
    return False

def valid_password(password: str) -> bool:
    if len(password) >= 6:
        return True
    return False

def valid_first_name(name_first: str) -> bool:
    # check first name length is in [1, 50]
    if len(name_first) in range(1, 50):
        return True
    return False

def valid_last_name(name_last: str) -> bool:
    # check last name length is in [1, 50]
    if len(name_last) in range(1, 50):
        return True
    return False

def email_exists(email: str) -> bool:
    # check if email already exists in data
    for user in data['users']:
        if user['email'] == email:
            return True
    return False

def valid_channel_name(name: str) -> bool:
    if len(name) > 20:
        return True
    return False