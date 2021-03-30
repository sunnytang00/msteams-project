import pytest

from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from src.base.dm import dm_create
from tests.helper import clear

@clear
def test_dm_create_single():
    """TODO"""
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user_id = user.get('auth_user_id')
    u_ids = [user_id]

    dm_id = 1
    dm_name = "harrypotter"
    assert dm_create(u_ids) == {dm_id, dm_name}

@clear
def test_dm_create_many():
    """TODO"""
    # TODO make this test better, add more stuff
    user1 = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user1_id = user1.get('auth_user_id')

    user2 = auth_register_v1(email='bobsmith@gmail.com',
                            password='askdflj29',
                            name_first='Bob',
                            name_last='Smith')
    user2_id = user2.get('auth_user_id')

    user3 = auth_register_v1(email='bobsmith2@gmail.com',
                            password='jfaDdf2@99',
                            name_first='Bob',
                            name_last='Smith')
    user3_id = user3.get('auth_user_id')

    u_ids = [user1_id, user2_id, user3_id]

    dm_id = 1
    dm_name = "bobsmith, bobsmith0, harrypotter"
    assert dm_create(u_ids) == {dm_id, dm_name}