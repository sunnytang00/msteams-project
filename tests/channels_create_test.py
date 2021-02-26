import pytest
from src.channels import channels_create
from src.data import data

def 

def test_vaild_input:
    channel_len = len(data['channels'])
    channel_id = channel_len + 1
    assert channels_create_v1(channel_id, "correct", True) == {}

def test_name_length:
    channel_len = len(data['channels'])
    channel_id = channel_len + 1
    with pytest.rasie(InputError) as e: 
        channels_create_v1(channel_id, "first channel" * 10, True)
        assert 'Name is too long' in str(e)

