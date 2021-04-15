import pytest
from src.echo import echo
from src.error import InputError

def test_echo_echo():
    with pytest.raises(InputError):
        echo('echo')

def test_echo_succes():
    assert echo('1') == '1'
