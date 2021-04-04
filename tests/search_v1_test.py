""" TODO : add test cases for dms """
"""
from src.base.error import InputError, AccessError
from src.base.message import message_send_v1, message_remove_v1, message_edit_v1
import pytest
from tests.helper import helper, clear
from src.base.other import search_v1
from src.base.auth import auth_register_v1

@clear
def test_no_channels(helper):
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    auth_user_id = user['auth_user_id']

    with pytest.raises(InputError) as e:
        search_v1(auth_user_id, "Hello")
        assert 'You are do not have any dms and are not in any channels' in str(e.value)


@clear
def test_empty_query_str(helper):
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    auth_user_id = user['auth_user_id']

    ch1 = channels_create_v1(auth_user_id, "test channel", True)['channel_id']
    channel_id = channel['channel_id']

    with pytest.raises(InputError) as e:
        search_v1(auth_user_id, "")
        assert 'Query string is empty' in str(e.value)

@clear
def test_invalid_auth_user_id():
    with pytest.raises(InputError) as e:
        search_v1('NotValid', "Hello")
        assert 'Auth_user_id is not real' in str(e.value)

@clear
def test_query_too_long(helper):
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    auth_user_id = user['auth_user_id']
    with pytest.raises(InputError) as e:
        search_v1(auth_user_id, "F" * 1001)
        assert 'Query string is too long' in str(e.value)

@clear 
def test_no_match(helper):

    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    auth_user_id = user['auth_user_id']

    test_channel = channels_create_v1(auth_user_id, "test channel", True)['channel_id']
    channel_id = channel['channel_id']

    message_send_v1(auth_user_id, channel_id, "Hello1")

    assert search_v1(auth_user_id, "Hello") == {'messages':[]}

@clear 
def test_one_match(helper):

    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    auth_user_id = user['auth_user_id']

    test_channel = channels_create_v1(auth_user_id, "correct", True)['channel_id']

    message_send_v1(auth_user_id, channel_id, "Hello")

    result = search_v1(auth_user_id, "Hello")
    assert len(result['messages']) == 1

@clear 
def test_many_matches(helper):

    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    auth_user_id = user['auth_user_id']

    ch1 = channels_create_v1(auth_user_id, "test channel", True)['channel_id']
    channel_id = channel['channel_id']

    message_send_v1(auth_user_id, channel_id, "Hello")
    message_send_v1(auth_user_id, channel_id, "Hello")
    message_send_v1(auth_user_id, channel_id, "Hello")
    message_send_v1(auth_user_id, channel_id, "Hello")
    message_send_v1(auth_user_id, channel_id, "Hello")

    result = search_v1(auth_user_id, "Hello")
    assert len(result['messages']) == 5

"""