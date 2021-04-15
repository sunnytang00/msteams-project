import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_list_v1
from tests.helper import clear

@clear
def test_valid_input():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    auth_user_id = user.get('auth_user_id')

    dm = dm_create_v1(auth_user_id, [])

    #should replaced when dm_details() finished
    dms = dm_list_v1(auth_user_id)
    dm_id = dm['dm_id']
    assert dm_id in [dm['dm_id'] for dm in dms]

@clear
def test_not_member_of_any_dm():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    auth_user_id = user.get('auth_user_id')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user2_id = user2['auth_user_id']
    user3 = auth_register_v1(email='harrypotter1@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user3_id = user3['auth_user_id']
    user4 = auth_register_v1(email='harrypotter2@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user4_id = user4['auth_user_id']


    dm_create_v1(auth_user_id, [user3_id, user4_id])

    #should replaced when dm_details() finished
    dms = dm_list_v1(user2_id)
    expected = []

    assert expected == dms

@clear
def test_more_user_in_dm():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    auth_user_id = user.get('auth_user_id')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    u_id = user2['auth_user_id']
    user3 = auth_register_v1(email='harrypotter1@gmail.com',
                                    password='qw3rtyAppl3s@99',
                                    name_first='Harry',
                                    name_last='Potter')
    user3_id = user3['auth_user_id']

    dm = dm_create_v1(auth_user_id, [u_id, user3_id])
    dms = dm_list_v1(auth_user_id)
    dm_id = dm['dm_id']

    assert dm_id in [dm['dm_id'] for dm in dms]

@clear
def test_invalid_token():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    auth_user_id = user.get('auth_user_id')

    #make a invalid id
    u_id = auth_user_id + 10

    with pytest.raises(AccessError) as e:
        dm_list_v1(u_id)
        assert f"token {u_id} does not refer to a valid user" in str(e.value)