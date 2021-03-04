import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from .helper import helper

def test_valid_input(helper):
    clear_v1()
    users_count = helper.get_users_count()
    helper.register_users(quantity=users_count)

    user_id = users_count + 1
    result = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    assert result == { 'auth_user_id': user_id }

def test_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1(email='this_is_not_an_email',
                        password='f3Fs$1l2z/A',
                        name_first='Steve',
                        name_last='Harvey')

def test_duplicate_email():
    """Register one user with an email, then try register a second user with the same email."""
    clear_v1()
    email = 'bobsmith@gmail.com'

    auth_register_v1(email=email,
                    password='K0zvR0xopjfv',
                    name_first='Bob',
                    name_last='Smith')

    with pytest.raises(InputError) as e:
        auth_register_v1(email=email,
                        password='ohIT8j2BB37s',
                        name_first='Bob',
                        name_last='Smith')
        assert 'Invalid email.' in str(e)

def test_short_password():
    """Test if user's password length is greater or equal to than 6."""
    clear_v1()
    with pytest.raises(InputError) as e:
        auth_register_v1(email='dragonslayer_44@gmail.com',
                        password='a'*5,
                        name_first='Timmy',
                        name_last='Randy')
        assert 'Password is too short.' in str(e)

    clear_v1()
    with pytest.raises(InputError) as e:
        auth_register_v1(email='erniesingleton@gmail.com',
                        password='4sjO3',
                        name_first='Ernie',
                        name_last='Singleton')
        assert 'Password is too short.' in str(e)

def test_first_name_length():
    """Test if user's first name is NOT in [1, 50]."""

    # test if first name is over 50 characters
    clear_v1()
    with pytest.raises(InputError) as e:
        auth_register_v1(email='aaaa_frazier@outlook.com',
                        password='mgQoU2YJpJyOTe4',
                        name_first='a'*50,
                        name_last='Frazier')
        assert 'First name invalid length.' in str(e)

    # test if first name is 0 characters
    clear_v1()
    with pytest.raises(InputError) as e:
        auth_register_v1(email='everett44@outlook.com',
                        password='mgQoU2YJpJyOTe4',
                        name_first='',
                        name_last='Everett')
        assert 'First name invalid length.' in str(e)

def test_last_name_length():
    """Test if user's last name is NOT in [1, 50]."""

    # test if last name is over 50 characters
    clear_v1()
    with pytest.raises(InputError) as e:
        auth_register_v1(email='oakley55@outlook.com',
                        password='mgQoU2YJpJyOTe4',
                        name_first='Oakley',
                        name_last='a'*50)
        assert 'Last name invalid length.' in str(e)

    # test if last name is 0 characters
    clear_v1()
    with pytest.raises(InputError) as e:
        auth_register_v1(email='Everett55@outlook.com',
                        password='9jx#v44yOTe4',
                        name_first='Everett',
                        name_last='')
        assert 'Last name invalid length.' in str(e)