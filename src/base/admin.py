from src.base.error import InputError, AccessError
from src.base.helper import get_user, user_is_Dream_owner
from src.data.helper import update_permission_id

def admin_userpermission_change_v1(auth_user_id, u_id, permission_id):
    if not get_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_user(u_id):
        raise InputError(f'u_id {u_id} does not refer to a valid user id')

    if not permission_id == 1 and not permission_id == 2:
        raise InputError(f'permission_id {permission_id} does not refer to a valid permisison id')

    if not user_is_Dream_owner(auth_user_id):
        raise AccessError(f'user id {auth_user_id} is not owner of Dreams')
    
    update_permission_id(u_id, permission_id)

    return {}