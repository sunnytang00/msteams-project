import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_remove_v1, dm_leave_v1
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
    dm = dm_create_v1(auth_user_id, [user2_id, user3_id])

    dm_id = dm.get('dm_id')
    assert dm_id == 1
    #what happens if creator wants to leave??? ASK ANTO
    dm_leave_v1(user2_id, dm_id)

    assert get_dm(dm_id).get('u_ids') == [1, 3]

@clear
def test_dm_id_not_valid():
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
    dm = dm_create_v1(auth_user_id, [user2_id, user3_id])

    dm_id = dm.get('dm_id')
    assert dm_id == 1
    fake_dm_id = 2

    with pytest.raises(InputError) as e:
        dm_leave_v1(user2_id, fake_dm_id)
        assert f"dm_id {fake_dm_id} does not refer to a valid dm" in str(e.value)

@clear
def test_member_not_part_of_dm():
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
    user4 = auth_register_v1(email='harrypotter112221@gmail.com',
                            password='qw3rtyApld@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')
    user3_id = user3.get('auth_user_id')
    user4_id = user4.get('auth_user.id')

    #create a dm
    dm = dm_create_v1(auth_user_id, [user2_id, user3_id])

    dm_id = dm.get('dm_id')
    assert dm_id == 1

    with pytest.raises(AccessError) as e:
        dm_leave_v1(user4_id, dm_id)
        assert f"auth_user {user4_id} is not member of dm {dm_id}" in str(e.value)
