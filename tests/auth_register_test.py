import pytest
from src.auth import auth_register_v1
from src.data import data
from src.error import InputError

def test_valid_input():
    data_len = len(data)
    user_id = data_len + 1
    assert auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter') == {'auth_user_id': user_id}

def test_echo_except():
    with pytest.raises(InputError):
        auth_register_v1(email='this_is_not_an_email',
            password='f3Fs$1l2z/A',
            name_first='Steve',
            name_last='Harvey')