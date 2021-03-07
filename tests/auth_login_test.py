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

def test_manymore_users_success():
    """Testing registering a large amount of users, then logging in with one"""
    clear_v1()
    auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@01',
                        name_first='Harry',
                        name_last='Potter')

    auth_register_v1(email='harrypotter1@gmail.com',
                        password='qw3rtyAppl3s@02',
                        name_first='Harrry',
                        name_last='Pottter')

    auth_register_v1(email='harrypotter2@gmail.com',
                        password='qw3rtyAppl3s@03',
                        name_first='Harrrry',
                        name_last='Potttter')

    result = auth_register_v1(email='harrypotter3@gmail.com',
                        password='qw3rtyAppl3s@04',
                        name_first='Harrrrry',
                        name_last='Pottttter')

    auth_register_v1(email='harrypotter4@gmail.com',
                        password='qw3rtyAppl3s@05',
                        name_first='Harrrrrry',
                        name_last='Potttttter')

    auth_register_v1(email='harrypotter5@gmail.com',
                        password='qw3rtyAppl3s@06',
                        name_first='Harrrrrrry',
                        name_last='Pottttttter')

    auth_register_v1(email='harrypotter6@gmail.com',
                        password='qw3rtyAppl3s@07',
                        name_first='Harrrrrrrry',
                        name_last='Potttttttter')

    auth_register_v1(email='harrypotter7@gmail.com',
                        password='qw3rtyAppl3s@08',
                        name_first='Harrrrrrrrry',
                        name_last='Pottttttttter')

    auth_register_v1(email='harrypotter8@gmail.com',
                        password='qw3rtyAppl3s@09',
                        name_first='Harrrrrrrrrry',
                        name_last='Potttttttttttter')

    auth_register_v1(email='harrypotter9@gmail.com',
                        password='qw3rtyAppl3s@10',
                        name_first='Harrrrrrrrrrry',
                        name_last='Pottttttttttttttter')

    auth_register_v1(email='harrypotter10@gmail.com',
                        password='qw3rtyAppl3s@11',
                        name_first='Harrrrrrrrrrrry',
                        name_last='Potttttttttttttttttter')

    auth_register_v1(email='harrypotter11@gmail.com',
                        password='qw3rtyAppl3s@12',
                        name_first='Harrrrrrrrrrrrry',
                        name_last='Potttttttttttttttttttter')

    assert auth_login_v1(email='harrypotter3@gmail.com',
                            password='qw3rtyAppl3s@04') == result

def test_many_logins():
    """Testing registering a large amount of users, then logging in with one"""
    clear_v1()
    auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@01',
                        name_first='Harry',
                        name_last='Potter')

    auth_register_v1(email='harrypotter1@gmail.com',
                        password='qw3rtyAppl3s@02',
                        name_first='Harrry',
                        name_last='Pottter')

    auth_register_v1(email='harrypotter2@gmail.com',
                        password='qw3rtyAppl3s@03',
                        name_first='Harrrry',
                        name_last='Potttter')

    result1 = auth_register_v1(email='harrypotter3@gmail.com',
                        password='qw3rtyAppl3s@04',
                        name_first='Harrrrry',
                        name_last='Pottttter')

    auth_register_v1(email='harrypotter4@gmail.com',
                        password='qw3rtyAppl3s@05',
                        name_first='Harrrrrry',
                        name_last='Potttttter')

    result2 = auth_register_v1(email='harrypotter5@gmail.com',
                        password='qw3rtyAppl3s@06',
                        name_first='Harrrrrrry',
                        name_last='Pottttttter')

    auth_register_v1(email='harrypotter6@gmail.com',
                        password='qw3rtyAppl3s@07',
                        name_first='Harrrrrrrry',
                        name_last='Potttttttter')

    auth_register_v1(email='harrypotter7@gmail.com',
                        password='qw3rtyAppl3s@08',
                        name_first='Harrrrrrrrry',
                        name_last='Pottttttttter')

    auth_register_v1(email='harrypotter8@gmail.com',
                        password='qw3rtyAppl3s@09',
                        name_first='Harrrrrrrrrry',
                        name_last='Potttttttttttter')

    auth_register_v1(email='harrypotter9@gmail.com',
                        password='qw3rtyAppl3s@10',
                        name_first='Harrrrrrrrrrry',
                        name_last='Pottttttttttttttter')

    result3= auth_register_v1(email='harrypotter10@gmail.com',
                        password='qw3rtyAppl3s@11',
                        name_first='Harrrrrrrrrrrry',
                        name_last='Potttttttttttttttttter')

    auth_register_v1(email='harrypotter11@gmail.com',
                        password='qw3rtyAppl3s@12',
                        name_first='Harrrrrrrrrrrrry',
                        name_last='Potttttttttttttttttttter')

    assert auth_login_v1(email='harrypotter3@gmail.com',
                            password='qw3rtyAppl3s@04') == result1

    assert auth_login_v1(email='harrypotter5@gmail.com',
                            password='qw3rtyAppl3s@06') == result2

    assert auth_login_v1(email='harrypotter10@gmail.com',
                            password='qw3rtyAppl3s@11') == result3

def test_manymore_users_fail():
    """Testing registering a large amount of users, then logging in with one"""
    clear_v1()
    auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@01',
                        name_first='Harry',
                        name_last='Potter')

    auth_register_v1(email='harrypotter1@gmail.com',
                        password='qw3rtyAppl3s@02',
                        name_first='Harrry',
                        name_last='Pottter')

    auth_register_v1(email='harrypotter2@gmail.com',
                        password='qw3rtyAppl3s@03',
                        name_first='Harrrry',
                        name_last='Potttter')

    result = auth_register_v1(email='harrypotter3@gmail.com',
                        password='qw3rtyAppl3s@04',
                        name_first='Harrrrry',
                        name_last='Pottttter')

    auth_register_v1(email='harrypotter4@gmail.com',
                        password='qw3rtyAppl3s@05',
                        name_first='Harrrrrry',
                        name_last='Potttttter')

    auth_register_v1(email='harrypotter5@gmail.com',
                        password='qw3rtyAppl3s@06',
                        name_first='Harrrrrrry',
                        name_last='Pottttttter')

    auth_register_v1(email='harrypotter6@gmail.com',
                        password='qw3rtyAppl3s@07',
                        name_first='Harrrrrrrry',
                        name_last='Potttttttter')

    auth_register_v1(email='harrypotter7@gmail.com',
                        password='qw3rtyAppl3s@08',
                        name_first='Harrrrrrrrry',
                        name_last='Pottttttttter')

    auth_register_v1(email='harrypotter8@gmail.com',
                        password='qw3rtyAppl3s@09',
                        name_first='Harrrrrrrrrry',
                        name_last='Potttttttttttter')

    auth_register_v1(email='harrypotter9@gmail.com',
                        password='qw3rtyAppl3s@10',
                        name_first='Harrrrrrrrrrry',
                        name_last='Pottttttttttttttter')

    auth_register_v1(email='harrypotter10@gmail.com',
                        password='qw3rtyAppl3s@11',
                        name_first='Harrrrrrrrrrrry',
                        name_last='Potttttttttttttttttter')
  
    auth_register_v1(email='harrypotter11@gmail.com',
                        password='qw3rtyAppl3s@12',
                        name_first='Harrrrrrrrrrrrry',
                        name_last='Potttttttttttttttttttter')

    with pytest.raises(InputError) as e:
        auth_login_v1(email='harryswrongemail.com',
                            password='verywrongpassword')
        
        assert 'Email does not belong to a user.' in str(e)









