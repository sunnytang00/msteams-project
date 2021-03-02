import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError

def test_users_clear():
    clear_v1()

    result = auth_register_v1(email='batman@gmail.com',
                        password='q3yAppl3s99',
                        name_first='Bat',
                        name_last='Man')
    clear_v1()

    cleared_result = auth_register_v1(email='maxwell_casper222@gmail.com',
                        password='q3yAppl3s99',
                        name_first='Casper ',
                        name_last='Maxwell')
    assert result == cleared_result

"""
def test_clear_channels():
    pass
"""