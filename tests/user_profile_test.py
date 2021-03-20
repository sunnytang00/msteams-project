import pytest
from src.base.auth import auth_register_v1
from src.base.user import user_profile_v1
from src.base.other import clear_v1
from src.base.error import InputError
from tests.helper import helper

def test_single_user():
    """Get user profile a database with only one user requesting its own profile."""
    clear_v1()
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first='Harry'
    name_last='Potter'
    handle_str = 'harrypotter'

    user = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user_auth_id = user['auth_user_id']
    assert user_auth_id == 1

    expected = {email, password, name_first, name_last, handle_str}
    assert user_profile_v1(user_auth_id, user_auth_id) == expected

# TODO: test valid if user is valid
