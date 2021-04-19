import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_remove_v1, dm_list_v1
from tests.helper import clear
#from src.data.helper import get_dms

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

    assert dm.get('dm_id') == 1
    
    dm_remove_v1(auth_user_id, 1)

    assert dm_list_v1(auth_user_id) == []

@clear
def test_same_dm_owner_remove_one():
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
    dm1 = dm_create_v1(auth_user_id, [user2_id, user3_id])

    assert dm.get('dm_id') == 1
    assert dm1.get('dm_id') == 2
    
    dm_remove_v1(auth_user_id, 1)
    lst = [dm['dm_id'] for dm in dm_list_v1(auth_user_id)]
    assert lst == [2]
    '''
    assert get_dms() == [{
        'auth_user_id' : 1,
        'dm_id' : 2,
        'dm_name' : 'harrypotter, harrypotter0, harrypotter1',
        'u_ids' : [2, 3],
        'messages': []
    }]
    '''
@clear
def test_create_two_dm_remove_one():
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
    dm1 = dm_create_v1(user2_id, [user2_id, user3_id])

    assert dm.get('dm_id') == 1
    assert dm1.get('dm_id') == 2
    
    dm_remove_v1(user2_id, 2)
    lst = [dm['dm_id'] for dm in dm_list_v1(auth_user_id)]
    assert lst == [1]

    '''
    assert get_dms() == [{
        'auth_user_id' : 1,
        'dm_id' : 1,
        'dm_name' : 'harrypotter, harrypotter0, harrypotter1',
        'u_ids' : [2, 3],
        'messages': []
    }]
    '''
@clear
def test_not_valid_dm_id():
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
    
    with pytest.raises(InputError) as e:
        dm_remove_v1(auth_user_id, 2)
        assert f"dm_id {dm_id} does not refer to a valid dm" in str(e.value)

@clear
def test_not_creator_deleting_dm():
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

    assert dm.get('dm_id') == 1
    
    with pytest.raises(AccessError) as e:
        dm_remove_v1(user2_id, 1)
        assert f'auth_user_id with auth_user_id {user2_id} is not creator' in str(e.value)
