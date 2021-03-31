"""TODO"""

from src.base.error import InputError
from src.base.helper import get_dm_name
from src.data.helper import get_dm_count, store_dm

def dm_create(auth_user_id, u_ids):
    """TODO"""
    #using auth user in place of token
    dm_id = get_dm_count() + 1
    dm_name = get_dm_name(u_ids)
    dm = {
        'auth_user_id' : auth_user_id,
        'dm_id': dm_id,
        'dm_name:': dm_name,
        'u_ids': u_ids
    }
    store_dm(dm)

    return {
        'dm_id': 1,
        'dm_name': dm_name
    }