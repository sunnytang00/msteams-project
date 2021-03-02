import pytest
from src.auth import auth_register_v1
from src.data import data
from src.error import InputError

def test_valid_input():
    user_id = len(data['users']) + 1
    assert auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter') == {'auth_user_id': user_id}

def test_invalid_email():
    with pytest.raises(InputError):
        auth_register_v1(email='this_is_not_an_email',
                        password='f3Fs$1l2z/A',
                        name_first='Steve',
                        name_last='Harvey')

def test_duplicate_email():
    """
    Register one user with an email, then try
    register a second user with the same email.
    """
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
    with pytest.raises(InputError) as e:
        auth_register_v1(email='erniesingleton@gmail.com',
                        password='4sjO3',
                        name_first='Ernie',
                        name_last='Singleton')
        assert 'Password is too short.' in str(e)


def test_first_name_length():
    """Test if user's first name is NOT in [1, 50]."""
    with pytest.raises(InputError) as e:
        auth_register_v1(email='Ovuvuevuevue@outlook.com',
                        password='mgQoU2YJpJyOTe4',
                        name_first='Ovuvuevuevue-Enyetuenwuevue-Ugbemugbem-Osasosasosasosasosas',
                        name_last='Abioye')
        assert 'First name is too long.' in str(e)

def test_last_name_length():
    """Test if user's last name is NOT in [1, 50]."""
    with pytest.raises(InputError) as e:
        auth_register_v1(email='huber.w@gmail.com',
                        password='TQqNTwxXad6Rj7',
                        name_first='Hubert',
                        name_last='Wolfeschlegelsteinhausenbergerdorffrste­erdemensch­der­raumschiff­')
        assert 'Last name is too long.' in str(e)
