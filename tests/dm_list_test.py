import pytest

from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from src.base.dm import dm_create, dm_list_v1
from tests.helper import clear

def test_valid_input():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user_id = user.get('auth_user_id')

    dm = dm_create(user_id)

    #should replaced when dm_details() finished
    dms = dm_list_v1(user_id)
    expected = [dm]

    assert expected == dms

def test_not_member_of_any_dm():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user_id = user.get('auth_user_id')
    user2 = auth_register_v1(email='harrypotter7@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user2['auth_user_id']

    dm = dm_create(user_id)

    #should replaced when dm_details() finished
    dms = dm_list_v1(u_id)
    expected = []

    assert expected == dms