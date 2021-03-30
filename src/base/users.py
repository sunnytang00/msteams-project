#from src.data.helper import get_users
'''
the function got changed since the change of user structure
pervious version: return all users
current version: return all users except those being removed
'''
from src.base.helper import get_current_users
def users_all_v1():
    return get_current_users()
