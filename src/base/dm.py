"""TODO"""

from src.base.error import InputError, AccessError
from src.base.helper import get_dm_name, get_current_user, get_dm, user_is_dm_member, get_user
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
        'u_ids': u_ids,
        'messages': []
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

def dm_details_v1(auth_user_id, dm_id):
    """TODO"""
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")

    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f"auth_user {auth_user_id} is not member of dm {dm_id}")

    dm = get_dm(dm_id)
    members = []
    for u_id in dm['u_ids']:
        user = get_user(u_id)
        if user:
            members.append(user)
    
    return {'name': dm['dm_name'], 'members': members}

def Func_for_sort_msg(msgs):
    return msgs['message_id']

def dm_messages_v1(auth_user_id, dm_id, start):
    """TODO"""
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")

    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f"auth_user {auth_user_id} is not member of dm {dm_id}")

    msgs = get_dm(dm_id).get('messages').copy()

    if start > len(msgs):
        raise InputError(f"the message in dm is less than {start}")

    msgs.sort(reverse = True, key = Func_for_sort_msg)

    end = -1
    if len(msgs) > (start + 50):
        end = start + 50

    messages  = msgs[start : end]

    return {
        'messages': messages,
        'start': start,
        'end': end
    }