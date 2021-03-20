import pytest
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from src.base.error import InputError
from tests.helper import helper
from src.base.user import user_profile_v1, user_profile_sethandle_v1, user_profile_setname_v1
from src.base.helper import get_handle_str

def test_single_user():
    
    clear_v1()
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first = 'Harry'
    name_last = 'Potter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1
    u_id = 1

    new_handle = 'testhandle'

    user_profile_sethandle_v1(auth_user_id, new_handle)

    assert user_profile_v1(auth_user_id, u_id).get('user').get('handle_str') == new_handle

def test_two_character_handle_string():
    
    clear_v1()
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first = 'Harry'
    name_last = 'Potter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1
    
    new_handle = '22'

    with pytest.raises(InputError) as e:

        user_profile_sethandle_v1(auth_user_id, new_handle)

        assert f'Handle string {new_handle} is not between 3 and 20 characters inclusive' in str(e)

def test_21_character_handle_string():
    
    clear_v1()
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first = 'Harry'
    name_last = 'Potter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1

    new_handle = '2' * 21

    with pytest.raises(InputError) as e:

        user_profile_sethandle_v1(auth_user_id, new_handle)

        assert f'Handle string {new_handle} is not between 3 and 20 characters inclusive' in str(e)

def test_handle_string_in_use():
    
    clear_v1()
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first = 'Harry'
    name_last = 'Potter'

    email1 = 'severussnape@gmail.com'
    password1 = 'potter'
    name_first1='Severus'
    name_last1='Snape'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)

    auth_register_v1(email=email1,
                            password=password1,
                            name_first=name_first1,
                            name_last=name_last1)

    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1

    new_handle = 'severussnape'

    with pytest.raises(InputError) as e:
        user_profile_sethandle_v1(auth_user_id, new_handle)
        assert f'Handle string {new_handle} is already in use' in str(e)     
