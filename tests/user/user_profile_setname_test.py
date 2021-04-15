import pytest
from src.auth import auth_register_v1
from src.user import user_profile_setname_v1, user_profile_v1
from src.other import clear_v1
from src.error import InputError
from tests.helper import helper, clear


@clear
def test_single_user():
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first='Harry'
    name_last='Potter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1
    u_id = 1

    new_name_first = 'Albus'
    new_name_last = 'Dumbledore'

    user_profile_setname_v1(auth_user_id, new_name_first, new_name_last)

    assert user_profile_v1(auth_user_id, u_id).get('user').get('name_first') == new_name_first
    assert user_profile_v1(auth_user_id, u_id).get('user').get('name_last') == new_name_last

@clear
def test_invalid_firstname_change():
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first='Harry'
    name_last='Potter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1

    new_name_first = 'a' * 51
    new_name_last = 'Dumbledore'

    with pytest.raises(InputError) as e:
        user_profile_setname_v1(auth_user_id, new_name_first, new_name_last)

        assert f'name_first {new_name_first} is not between 1 and 50 characters inclusively in length' in str(e.value)

@clear
def test_invalid_lastname_change():
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first='Harry'
    name_last='Potter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1

    new_name_first = 'Albus'
    new_name_last = 'a' * 51

    with pytest.raises(InputError) as e:
        user_profile_setname_v1(auth_user_id, new_name_first, new_name_last)
        assert f'name_last {new_name_last} is not between 1 and 50 characters inclusively in length' in str(e.value)        
