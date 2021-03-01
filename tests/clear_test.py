import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.data import data
from src.error import InputError

def test_regular_clear():
    clear_v1()
    assert len(data['users']) == 0 # and len(data['channels']) == 0

def test_users_clear():
    auth_register_v1(email='batman@gmail.com',
                        password='q3yAppl3s99',
                        name_first='Bat',
                        name_last='Man')
    clear_v1()
    assert len(data['users']) == 0

"""
def test_clear_channels():
    pass
"""