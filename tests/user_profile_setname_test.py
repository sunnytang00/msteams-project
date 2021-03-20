import pytest
from src.base.auth import auth_register_v1
from src.base.user import user_profile_setname_v1
from src.base.other import clear_v1
from src.base.error import InputError
from tests.helper import helper
from src.base.user import user_profile_v1

def test_single_user():
    clear_v1()
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



