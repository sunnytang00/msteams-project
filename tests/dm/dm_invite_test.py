import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_invite_v1
from tests.helper import clear
from src.data.helper import get_dms
from src.helper import get_dm

@clear
def test_valid_input():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rt2Appl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user3 = auth_register_v1(email='harrypotter11111@gmail.com',
                            password='qw3rtyApl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')
    user3_id = user3.get('auth_user_id')

    #create a dm
    dm = dm_create_v1(auth_user_id, [user2_id])

    dm_id = dm.get('dm_id')
    assert dm_id == 1
    
    dm_invite_v1(auth_user_id, dm_id, user3_id)

    assert get_dm(dm_id).get('u_ids') == [1, 2, 3]

@clear
def test_invite_multiple():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rt2Appl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user3 = auth_register_v1(email='harrypotter11111@gmail.com',
                            password='qw3rtyApl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user4 = auth_register_v1(email='harrypotter2222@gmail.com',
                            password='qw3rtyApl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')
    user3_id = user3.get('auth_user_id')
    user4_id = user4.get('auth_user_id')

    #create a dm
    dm = dm_create_v1(auth_user_id, [user2_id])

    dm_id = dm.get('dm_id')
    assert dm_id == 1
    
    dm_invite_v1(auth_user_id, dm_id, user3_id)
    dm_invite_v1(auth_user_id, dm_id, user4_id)

    assert get_dm(dm_id).get('u_ids') == [1, 2, 3, 4]

@clear
def test_dm_not_exist():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rt2Appl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user3 = auth_register_v1(email='harrypotter11111@gmail.com',
                            password='qw3rtyApl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')
    user3_id = user3.get('auth_user_id')

    #create a dm
    dm = dm_create_v1(auth_user_id, [user2_id])

    dm_id = dm.get('dm_id')
    assert dm_id == 1

    fake_dm_id = 2

    with pytest.raises(InputError) as e:
        dm_invite_v1(auth_user_id, fake_dm_id, user3_id)
        assert f"dm_id {fake_dm_id} does not refer to a valid dm" in str(e.value)

@clear
def test_u_id_not_valid():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rt2Appl3s@99',
                            name_first='Harry',
                            name_last='Potter')


    auth_user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')
    fake_u_id = 99

    #create a dm
    dm = dm_create_v1(auth_user_id, [user2_id])

    dm_id = dm.get('dm_id')
    assert dm_id == 1

    with pytest.raises(InputError) as e:
        dm_invite_v1(auth_user_id, dm_id, fake_u_id)
        assert f"u_id {fake_u_id} does not refer to a valid user" in str(e.value)

@clear
def test_auth_not_member_of_dm():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rt2Appl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user3 = auth_register_v1(email='harrypotter11111@gmail.com',
                            password='qw3rtyApl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user4 = auth_register_v1(email='harrypotter2222@gmail.com',
                            password='qw3rtyApl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')
    user3_id = user3.get('auth_user_id')
    user4_id = user4.get('auth_user_id')

    #create a dm
    dm = dm_create_v1(auth_user_id, [user2_id])

    dm_id = dm.get('dm_id')
    assert dm_id == 1

    with pytest.raises(AccessError) as e:
        dm_invite_v1(user3_id, dm_id, user4_id)
        assert f'user with auth_user_id {user3_id} is not part of the dm' in str(e.value)

