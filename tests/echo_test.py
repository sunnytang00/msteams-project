import pytest
from src.base.echo import echo
from src.base.error import InputError

def test_echo_echo():
    with pytest.raises(InputError) as e:
        echo('echo')

def test_echo_succes():
    assert echo('1') == '1'
