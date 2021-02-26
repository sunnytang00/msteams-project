import pytest
from src.channels import channels_create_v1
from src.data import data
from src.error import InputError

def test_vaild_input():
    channel_len = len(data['channels'])
    channel_id = channel_len + 1
    assert channels_create_v1(channel_id, "correct", True) == {'channel_id': channel_id}

def test_name_length():
    channel_len = len(data['channels'])
    channel_id = channel_len + 1
    with pytest.raises(InputError) as e: 
        channels_create_v1(channel_id, "first channel" * 10, True)
        assert 'Name is too long' in str(e)

