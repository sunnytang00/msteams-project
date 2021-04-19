#from src.data.helper import get_users
'''
the function got changed since the change of user structure
pervious version: return all users
current version: return all users except those being removed
'''
from src.error import AccessError
from src.helper import get_current_users, get_current_user
def users_all_v1(auth_user_id: int):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    return get_current_users()
