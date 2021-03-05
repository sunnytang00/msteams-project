import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src.error import InputError

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
