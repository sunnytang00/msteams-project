import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from src.helper import get_handle_str
from tests.helper import helper, clear

@clear
def test_single_user():
    auth_user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    assert auth_user.get('auth_user_id') == 1

@clear
def test_invalid_email():
    invalid_email = 'this_is_not_an_email'
    with pytest.raises(InputError) as e:
        auth_register_v1(email=invalid_email,
                        password='f3Fs$1l2z/A',
                        name_first='Steve',
                        name_last='Harvey')
        assert f'Email {invalid_email} entered is not a valid email' in str(e.value)

@clear
def test_duplicate_email():
    """Register one user with an email, then try register a second user with the same email."""
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
        assert f'Email address {email} is already being used by another user' in str(e.value)

@clear
def test_short_password():
    """Test if user's password length is greater or equal to than 6."""
    invalid_password = 'a'*5
    with pytest.raises(InputError) as e:
        auth_register_v1(email='dragonslayer_44@gmail.com',
                        password=invalid_password,
                        name_first='Timmy',
                        name_last='Randy')
        assert f'Password {invalid_password} entered is less than 6 characters long' in str(e.value)

    clear_v1()
    invalid_password = '4sjO3'
    with pytest.raises(InputError) as e:
        auth_register_v1(email='erniesingleton@gmail.com',
                        password=invalid_password,
                        name_first='Ernie',
                        name_last='Singleton')
        assert f'Password {invalid_password} entered is less than 6 characters long' in str(e.value)

@clear
def test_first_name_length():
    """Test if user's first name is NOT in [1, 50]."""

    # test if first name is over 50 characters
    invalid_first_name = 'a'*51
    with pytest.raises(InputError) as e:
        auth_register_v1(email='aaaa_frazier@outlook.com',
                        password='mgQoU2YJpJyOTe4',
                        name_first=invalid_first_name,
                        name_last='Frazier')
        assert f'name_first {invalid_first_name} is not between 1 and 50 characters inclusively in length' in str(e.value)

    # test if first name is 0 characters
    clear_v1()
    invalid_first_name = ''
    with pytest.raises(InputError) as e:
        auth_register_v1(email='everett44@outlook.com',
                        password='mgQoU2YJpJyOTe4',
                        name_first=invalid_first_name,
                        name_last='Everett')
        assert f'name_first {invalid_first_name} is not between 1 and 50 characters inclusively in length' in str(e.value)

@clear
def test_last_name_length():
    """Test if user's last name is NOT in [1, 50]."""

    # test if last name is over 50 characters
    invalid_last_name = 'a'*51
    with pytest.raises(InputError) as e:
        auth_register_v1(email='oakley55@outlook.com',
                        password='mgQoU2YJpJyOTe4',
                        name_first='Oakley',
                        name_last=invalid_last_name)
        assert f'name_last {invalid_last_name} is not between 1 and 50 characters inclusively in length' in str(e.value)

    # test if last name is 0 characters
    clear_v1()
    invalid_last_name = '' 
    with pytest.raises(InputError) as e:
        auth_register_v1(email='Everett55@outlook.com',
                        password='9jx#v44yOTe4',
                        name_first='Everett',
                        name_last=invalid_last_name)
        assert f'name_last {invalid_last_name} is not between 1 and 50 characters inclusively in length' in str(e.value)

def test_regular_handle_str():
    name_first = 'Harry'
    name_last = 'Potter'

    output = get_handle_str(name_first, name_last)
    expected = 'harrypotter'
    assert expected == output

def test_uppercase_handle_str():
    name_first = 'HARRY'
    name_last = 'POTTER'

    output = get_handle_str(name_first, name_last)
    expected = 'harrypotter'
    assert expected == output

def test_long_handle_str():
    name_first = 'a'*50
    name_last = 'Potter'

    output = get_handle_str(name_first, name_last)
    expected = 'a'*20
    assert expected == output

def test_at_symbol_handle_str():
    name_first = 'Harry@@@@@@@@@@@@'
    name_last = 'Potter'

    output = get_handle_str(name_first, name_last)
    expected = 'harrypotter'
    assert expected == output

def test_mixed_handle_str():
    name_first = '@ r'*20
    name_last = 'Potter'

    output = get_handle_str(name_first, name_last)
    expected = 'r'*20
    assert expected == output

@clear
def test_already_taken_handle_str():
    auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    name_first = 'Harry'
    name_last = 'Potter'

    output = get_handle_str(name_first, name_last)
    expected = 'harrypotter0'
    assert expected == output

@clear
def test_many_taken_handle_str():
    auth_register_v1(email='harrypotter1@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    auth_register_v1(email='harrypotter2@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter0')
    auth_register_v1(email='harrypotter3@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter1')

    name_first = 'Harry'
    name_last = 'Potter'

    output = get_handle_str(name_first, name_last)
    expected = 'harrypotter2'
    assert expected == output

@clear
def test_taken_max_handle_str():
    auth_register_v1(email='harrypotter1@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='a'*20,
                            name_last='Potter')


    name_first = 'a'*20
    name_last = 'Potter'

    output = get_handle_str(name_first, name_last)
    expected = 'a'*20 + '0'
    assert expected == output
