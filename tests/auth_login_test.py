import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.data import data
from src.error import InputError

def test_valid_input():
    #Testing for a valid login, first register the user and then login, expected return is user_id
    auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user_id = len(data['users']) + 1

    assert auth_login_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99') == {'auth_user_id': user_id}
                          
def test_invalid_email():
    #Testing for an invalid email at login
    with pytest.raises(InputError) as e:

        auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

        auth_login_v1(email='this_is_not_an_email',
                                password='qw3rtyAppl3s@99') 

        assert 'Email is not valid.' in str(e)

def test_unknown_email():
    #Testing a non-registered email
    with pytest.raises(InputError):

        auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

        auth_login_v1(email='fake_email@gmail.com',
                            password='qw3rtyAppl3s@99')
        
        assert 'Email does not belong to a user.' in str(e)
     
def test_invalid_password():
    #Testing an invalid password
    with pytest.raises(InputError):

        auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

        auth_login_v1(email='harrypotter@gmail.com',
                        password='ffffffffF')  
        
        assert 'Password is not correct.' in str(e)

