"""TODO"""

from src.base.error import InputError, AccessError
from src.base.helper import get_dm_name, get_current_user, get_dm, user_is_dm_member
from src.data.helper import get_dm_count, store_dm, get_dms

def dm_create(auth_user_id, u_ids):
    """TODO"""
    #using auth user in place of token
    dm_id = get_dm_count() + 1
    dm_name = get_dm_name(u_ids)
    dm = {
        'auth_user_id' : auth_user_id,
        'dm_id': dm_id,
        'dm_name': dm_name,
        'u_ids': u_ids
    }
    store_dm(dm)

    return {
        'dm_id': 1,
        'dm_name': dm_name
    }

def dm_list_v1(auth_user_id):
    """TODO"""
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")
    
    dm_list = []
    for dm in get_dms():
        if user_is_dm_member(dm['dm_id'], auth_user_id):
            dm_list.append(get_dm(dm['dm_id']))

    return dm_list