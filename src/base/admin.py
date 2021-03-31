from src.base.error import InputError, AccessError
from src.base.helper import get_user, user_is_Dream_owner, remove_user, get_current_user
from src.data.helper import update_permission_id, get_owner_count, update_owner_count, update_removed_flag

def admin_userpermission_change_v1(auth_user_id, u_id, permission_id):
    if not get_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    if not get_current_user(u_id):
        raise InputError(f'u_id {u_id} does not refer to a valid user id')

    if not permission_id == 1 and not permission_id == 2:
        raise InputError(f'permission_id {permission_id} does not refer to a valid permisison id')

    if not user_is_Dream_owner(auth_user_id):
        raise AccessError(f'user id {auth_user_id} is not owner of Dreams')
    
    update_permission_id(u_id, permission_id)
    owner_count = get_owner_count() + 1
    update_owner_count(owner_count)

    return {}

def admin_user_remove_v1(auth_user_id, u_id):
    if not get_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid token")
    
    if not get_user(u_id):
        raise InputError(f"user_id {u_id} does not refer to a valid user")

    if not user_is_Dream_owner(auth_user_id):
        raise AccessError(f"user with user_id {u_id} is not owner of Dreams")

    if get_owner_count() == 1 and user_is_Dream_owner(u_id):
        raise InputError(f"user with user_id {u_id} is the only currently owner")

    update_removed_flag(u_id, True)

    if user_is_Dream_owner(u_id):
        owner_count = get_owner_count() - 1
        update_owner_count(owner_count)

    remove_user(u_id)
    
    return {}