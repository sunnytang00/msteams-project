"""TODO"""

from src.base.error import InputError
from src.base.helper import get_dm_name
from src.data.helper import get_dm_count, store_dm

def dm_create(u_ids):
    """TODO"""
    dm_id = get_dm_count() + 1
    dm_name = get_dm_name(u_ids)
    dm = {
        'dm_id': dm_id,
        'dm_name:': dm_name,
        'u_ids': u_ids
    }
    store_dm(dm)

    return {
        'dm_id': 1,
        'dm_name': dm_name
    }