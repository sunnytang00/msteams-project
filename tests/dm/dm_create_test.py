"""Tests for creating a DM"""

import pytest

from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1
from src.dm import dm_create_v1
from tests.helper import clear, helper

@clear
def test_dm_create_v1_single(helper):
    """Create a DM with a single user, not including owner"""
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    u_id = user.get('auth_user_id')
    auth_user_id = helper.register_user(1)
    assert u_id == 1
    assert auth_user_id == 2

    u_ids = [u_id]

    dm_id = 1
    dm_name = "harrrrrypottttter, harrypotter"
    assert dm_create_v1(auth_user_id, u_ids) == {'dm_id': dm_id, 'dm_name': dm_name}

@clear
def test_dm_create_v1_many():
    """Create many DMs with many users"""
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    u_id = user.get('auth_user_id')
    assert u_id == 1

    user2 = auth_register_v1(email='bobsmith@gmail.com',
                            password='askdflj29',
                            name_first='Bob',
                            name_last='Smith')
    u_id_2 = user2.get('auth_user_id')
    assert u_id_2 == 2

    user3 = auth_register_v1(email='bobsmith2@gmail.com',
                            password='jfaDdf2@99',
                            name_first='Bob',
                            name_last='Smith')
    u_id_3 = user3.get('auth_user_id')
    assert u_id_3 == 3 


    user4 = auth_register_v1(email='bobsmith3@gmail.com',
                            password='jfaDdf2@99',
                            name_first='Bob',
                            name_last='Smith')
    u_id_4 = user4.get('auth_user_id')
    assert u_id_4 == 4

    u_ids = [u_id, u_id_2, u_id_3]

    dm_id = 1
    dm_name = "bobsmith, bobsmith0, bobsmith1, harrypotter"
    assert dm_create_v1(u_id_4, u_ids) == {'dm_id': dm_id, 'dm_name': dm_name}

    # create second channel

    user5 = auth_register_v1(email='bobsmith4@gmail.com',
                            password='jfaDdf2@99',
                            name_first='Bob',
                            name_last='Smith')
    u_id_5 = user5.get('auth_user_id')
    assert u_id_5 == 5

    u_ids = [u_id_4, u_id_2, u_id_3, u_id_5]

    dm_id = 2
    dm_name = "bobsmith, bobsmith0, bobsmith1, bobsmith2, harrypotter"
    assert dm_create_v1(u_id, u_ids) == {'dm_id': dm_id, 'dm_name': dm_name}


@clear
def test_invalid_auth_user_id(helper):
    """test when u_id does not refer to a valid user"""
    auth_user_id = 45

    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    u_id = user.get('auth_user_id')

    u_ids = [u_id]

    with pytest.raises(InputError) as e:
        dm_create_v1(auth_user_id, u_ids)
    assert f"auth_user_id {auth_user_id} does not refer to a valid user" in str(e.value)

@clear
def test_invalid_u_ids(helper):
    """test u_id does not refer to a valid user"""
    auth_user_id = helper.register_user(1)

    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    u_id = user.get('auth_user_id')

    invalid_u_id = 24

    user3 = auth_register_v1(email='bobsmith@gmail.com',
                            password='askdflj29',
                            name_first='Bob',
                            name_last='Smith')
    u_id_3 = user3.get('auth_user_id')

    u_ids = [u_id, invalid_u_id, u_id_3]

    with pytest.raises(InputError) as e:
        dm_create_v1(auth_user_id, u_ids)
    assert f'u_id {invalid_u_id} does not refer to a valid user' in str(e.value)
