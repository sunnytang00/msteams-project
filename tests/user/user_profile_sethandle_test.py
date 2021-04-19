import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from tests.helper import helper, clear
from src.user import user_profile_v1, user_profile_sethandle_v1, user_profile_setname_v1
from src.helper import get_handle_str

@clear
def test_single_user():
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

@clear
def test_two_character_handle_string():
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

        assert f'Handle string {new_handle} is not between 3 and 20 characters inclusive' in str(e.value)

@clear
def test_21_character_handle_string():
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

        assert f'Handle string {new_handle} is not between 3 and 20 characters inclusive' in str(e.value)

@clear
def test_handle_string_in_use():
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
        assert f'Handle string {new_handle} is already in use' in str(e.value)     
