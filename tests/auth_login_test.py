import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src.error import InputError
from .helper import helper

def test_valid_input():
    """Testing for a valid login, first register the user and then login, expected return is user_id."""
    clear_v1()
    result = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    assert auth_login_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99') == result
                          

def test_many_users():
    """Register three users and try log middle one in."""
    clear_v1()
    auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@99',
                        name_first='Harry',
                        name_last='Potter')

    result = auth_register_v1(email='bob_smith@gmail.com',
                        password='jfs2@$sjxzvkl',
                        name_first='Bob',
                        name_last='Smith')

    auth_register_v1(email='fiza_good777@gmail.com',
                        password='qfjklj42w39',
                        name_first='Fiza',
                        name_last='Good')

    assert auth_login_v1(email='bob_smith@gmail.com',
                            password='jfs2@$sjxzvkl') == result

def test_unknown_email():
    """Testing a non-registered email."""
    clear_v1()
    auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@99',
                        name_first='Harry',
                        name_last='Potter')
    with pytest.raises(InputError) as e:
        auth_login_v1(email='fake_email@gmail.com',
                            password='qw3rtyAppl3s@99')
        
        assert 'Email does not belong to a user.' in str(e)
     
def test_invalid_password():
    """Testing an invalid password."""
    clear_v1()
    auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@99',
                        name_first='Harry',
                        name_last='Potter')

    with pytest.raises(InputError) as e:
        auth_login_v1(email='harrypotter@gmail.com',
                        password='ffffffffF')  
        assert 'Password is not correct.' in str(e)

def test_manymore_users_success(helper):
    """Testing registering a large amount of users, then logging in with one"""
    clear_v1()

    helper.register_users(10)

    result = auth_register_v1(email='harrypotter3@gmail.com',
                        password='qw3rtyAppl3s@04',
                        name_first='Harrrrry',
                        name_last='Pottttter')

    assert auth_login_v1(email='harrypotter3@gmail.com',
                            password='qw3rtyAppl3s@04') == result

def test_many_logins(helper):
    """Testing registering a large amount of users, then logging in with one"""
    clear_v1()

    helper.register_users(10)

    result1 = auth_register_v1(email='harrypotter3@gmail.com',
                        password='qw3rtyAppl3s@04',
                        name_first='Harrrrry',
                        name_last='Pottttter')

    result2 = auth_register_v1(email='harrypotter5@gmail.com',
                        password='qw3rtyAppl3s@06',
                        name_first='Harrrrrrry',
                        name_last='Pottttttter')

    result3 = auth_register_v1(email='harrypotter10@gmail.com',
                        password='qw3rtyAppl3s@11',
                        name_first='Harrrrrrrrrrrry',
                        name_last='Potttttttttttttttttter')

    assert auth_login_v1(email='harrypotter3@gmail.com',
                            password='qw3rtyAppl3s@04') == result1 and auth_login_v1(email='harrypotter5@gmail.com',
                            password='qw3rtyAppl3s@06') == result2 and auth_login_v1(email='harrypotter10@gmail.com',
                            password='qw3rtyAppl3s@11') == result3


def test_manymore_users_fail(helper):
    """Testing registering a large amount of users, then logging in with one"""
    clear_v1()

    helper.register_users(10)

    with pytest.raises(InputError) as e:
        auth_login_v1(email='harryswrongemail.com',
                            password='verywrongpassword')
        
        assert 'Email does not belong to a user.' in str(e)

def test_login_with_no_details(helper):

    clear_v1()

    auth_register_v1(email='harrypotter3@gmail.com',
                        password='qw3rtyAppl3s@04',
                        name_first='Harrrrry',
                        name_last='Pottttter')

    with pytest.raises(InputError) as e:
        auth_login_v1(email='',
                            password='')
        
        assert 'Email does not belong to a user.' in str(e)

def test_login_with_max_characters(helper):

    clear_v1()

    auth_register_v1(email='harrypotter3@gmail.com',
                        password='qw3rtyAppl3s@04',
                        name_first='Harrrrry',
                        name_last='Pottttter')

    with pytest.raises(InputError) as e:
        auth_login_v1(email='q'*10000,
                            password='q'*10000)
        
        assert 'Email does not belong to a user.' in str(e)










