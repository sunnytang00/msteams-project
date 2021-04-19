import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from tests.helper import helper, clear
from src.users import users_all_v1
from src.helper import get_handle_str 
from src.error import AccessError

@clear
def test_invalid_token(helper):
    invalid_id = 10

    with pytest.raises(AccessError) as e: 
        users_all_v1(auth_user_id=invalid_id)
        assert f'token {invalid_id} does not refer to a valid token' in str(e.value)

"""
@clear
def test_one_user(helper):

    helper.register_users(1)

    assert users_all_v1() == [{'u_id': 1, 
                                'email': 'harrypotter@gmail.com', 
                                'name_first': 'Harry', 
                                'name_last': 'Potter', 'handle_str': 
                                'harrypotter', 'password': 
                                'qw3rtyAppl3s@99', 'permission_id': 1, 
                                'removed' : False}]

@clear
def test_multiple_user(helper):

    helper.register_users(4)

    assert users_all_v1() == [{'u_id': 1, 
                                'email': 'harrypotter@gmail.com', 
                                'name_first': 'Harry', 
                                'name_last': 'Potter', 
                                'handle_str': 'harrypotter', 
                                'password': 'qw3rtyAppl3s@99', 'permission_id': 1,
                                'removed' : False}, 
                                {'u_id': 2, 
                                'email': 'bobsmith7@gmail.com', 
                                'name_first': 'Bob', 
                                'name_last': 'Smith', 
                                'handle_str': 'bobsmith', 
                                'password': 'K0zR0xopjfv', 'permission_id': 2,
                                'removed' : False}, 
                                {'u_id': 3, 
                                'email': 'gw9999@gmail.com', 
                                'name_first': 'Wiktoria', 
                                'name_last': 'Guerrero', 
                                'handle_str': 'wiktoriaguerrero', 
                                'password': 'K0zvR0xopjfv', 'permission_id': 2,
                                'removed' : False},
                                {'u_id': 4, 
                                'email': 'w3rren444@gmail.com', 
                                'name_first': 'Rhydian', 
                                'name_last': 'Warren', 
                                'handle_str': 'rhydianwarren', 
                                'password': 'K0z423xopjfv', 'permission_id': 2,
                                'removed' : False}]

@clear
def test_no_user():
    assert users_all_v1() == []
"""
