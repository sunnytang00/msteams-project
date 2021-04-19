import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src.error import InputError
from tests.helper import helper, clear

@clear
def test_valid_input(helper):
    """Testing for a valid login, first register the user and then login, expected return is auth_user_id."""
    output = auth_register_v1(email='harrypotter@gmail.com',
                                password='qw3rtyAppl3s@99',
                                name_first='Harry',
                                name_last='Potter')

    expected = auth_login_v1(email='harrypotter@gmail.com',
                                password='qw3rtyAppl3s@99')
    assert output.get('auth_user_id') == expected.get('auth_user_id') == 1

    output = auth_register_v1(email='harrypotter3@gmail.com',
                                password='qw3rtyAppl3s@04',
                                name_first='Harrrrry',
                                name_last='Pottttter')
    
    expected = auth_login_v1(email='harrypotter3@gmail.com',
                            password='qw3rtyAppl3s@04')
    assert output.get('auth_user_id') == expected.get('auth_user_id') == 2

@clear
def test_many_users(helper):
    """Register three users and try log middle one in."""
    helper.register_user(1)

    output = auth_register_v1(email='bob_smith@gmail.com',
                        password='jfs2@$sjxzvkl',
                        name_first='Bob',
                        name_last='Smith')
    helper.register_user(2)

    expected = auth_login_v1(email='bob_smith@gmail.com',
                                password='jfs2@$sjxzvkl')

    assert output.get('auth_user_id') == expected.get('auth_user_id')

@clear
def test_unknown_email():
    """Testing a non-registered email."""
    auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@99',
                        name_first='Harry',
                        name_last='Potter')

    invalid_email = 'fake_email@gmail.com'
    with pytest.raises(InputError) as e:
        auth_login_v1(email=invalid_email,
                        password='qw3rtyAppl3s@99')
        
        assert f'Email {invalid_email} entered does not belong to a user' in str(e.value)
     
@clear
def test_invalid_password():
    """Testing an invalid password."""
    auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@99',
                        name_first='Harry',
                        name_last='Potter')

    invalid_password = 'ffffffffF'
    with pytest.raises(InputError) as e:
        auth_login_v1(email='harrypotter@gmail.com',
                        password=invalid_password)  
        assert f'Password {invalid_password} is not correct.' in str(e.value)


@clear
def test_many_logins(helper):
    """Testing registering a large amount of users, then logging in with one"""
    helper.register_users(10)

    output1 = auth_register_v1(email='harrypotter3@gmail.com',
                                password='qw3rtyAppl3s@04',
                                name_first='Harrrrry',
                                name_last='Pottttter')

    output2 = auth_register_v1(email='harrypotter5@gmail.com',
                                password='qw3rtyAppl3s@06',
                                name_first='Harrrrrrry',
                                name_last='Pottttttter')

    output3 = auth_register_v1(email='harrypotter10@gmail.com',
                                password='qw3rtyAppl3s@11',
                                name_first='Harrrrrrrrrrrry',
                                name_last='Potttttttttttttttttter')

    assert auth_login_v1(email='harrypotter3@gmail.com',
                            password='qw3rtyAppl3s@04') == output1 and auth_login_v1(email='harrypotter5@gmail.com',
                            password='qw3rtyAppl3s@06') == output2 and auth_login_v1(email='harrypotter10@gmail.com',
                            password='qw3rtyAppl3s@11') == output3


@clear
def test_many_users_fail(helper):
    """Testing registering a large amount of users, then logging in with one"""
    helper.register_users(10)

    invalid_email = 'harryswrongemail.com'
    with pytest.raises(InputError) as e:
        auth_login_v1(email=invalid_email,
                            password='verywrongpassword')
        
        assert f'Email {invalid_email} does not belong to a user.' in str(e.value)

@clear
def test_no_details(helper):
    helper.register_users(15)
    empty_str = ''

    with pytest.raises(InputError) as e:
        auth_login_v1(email=empty_str,
                        password=empty_str)
        
        assert f'Email {empty_str} does not belong to a user.' in str(e.value)

@clear
def test_max_characters(helper):
    invalid_email = 'q'*1000
    with pytest.raises(InputError) as e:
        auth_login_v1(email=invalid_email,
                            password='fjk@40asj')
        
        assert f'Email {invalid_email} does not belong to a user.' in str(e.value)
