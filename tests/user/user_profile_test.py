import pytest
from src.auth import auth_register_v1
from src.user import user_profile_v1
from src.other import clear_v1
from src.error import InputError
from src.admin import admin_user_remove_v1
from tests.helper import helper, clear

@clear
def test_single_user():
    """Get user profile a database with only one user requesting its own profile."""
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first='Harry'
    name_last='Potter'
    handle_str = 'harrypotter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1
    u_id = 1

    expected = {'u_id': u_id, 
                'email': email,
                'name_first': name_first,
                'name_last': name_last,
                'handle_str': handle_str,
                'profile_img_url': ''
                }

    assert user_profile_v1(auth_user_id, u_id).get('user') == expected

@clear
def test_fail_user():
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
    u_id = 2
    with pytest.raises(InputError) as e:
        user_profile_v1(auth_user_id, u_id).get('user')
        assert f'User with u_id {u_id} is not a valid user' in str(e.value)

@clear
def test_removed_user(helper):
    auth_user_id = helper.register_user(1)
    u_id = helper.register_user(2)

    admin_user_remove_v1(auth_user_id, u_id)

    profile = user_profile_v1(auth_user_id, u_id).get('user')

    assert u_id == profile.get('u_id') and profile.get('name_first') == 'Removed' \
        and profile.get('name_last') == 'user'
