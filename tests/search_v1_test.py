from src.base.error import InputError, AccessError
from src.base.message import message_send_v1, message_remove_v1, message_edit_v1
import pytest
from tests.helper import helper, clear
from src.base.other import search_v1
from src.base.auth import auth_register_v1
from src.base.channels import channels_create_v1

@clear
def test_empty_query_str():
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']
    
    with pytest.raises(InputError) as e:
        search_v1(user_id, "")
        assert 'Query string is empty' in str(e.value)

@clear
def test_invalid_auth_user_id_int():
    with pytest.raises(InputError) as e:
        search_v1(-1, "Hello")
        assert 'Auth_user_id is not real' in str(e)

@clear
def test_invalid_auth_user_id_str():
    with pytest.raises(InputError) as e:
        search_v1('NotValid', "Hello")
        assert 'Auth_user_id is not real' in str(e)

@clear
def test_query_too_long():
    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']
    with pytest.raises(InputError) as e:
        search_v1(user_id, "F" * 1001)
        assert 'Query string is too long' in str(e)

@clear 
def test_no_match():

    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']

    test_channel = channels_create_v1(user_id, "test channel", True)
    channel_id = test_channel['channel_id']

    message_send_v1(user_id, channel_id, "Hello")

    assert search_v1(user_id, "Hello1") == []

@clear 
def test_one_match():

    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']

    test_channel = channels_create_v1(user_id, "correct", True)
    channel_id = test_channel['channel_id']

    message_send_v1(user_id, channel_id, "Hello")

    result = search_v1(user_id, "Hello")
    assert len(result) == 1

@clear 
def test_not_in_a_channel():

    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']

    user1 = auth_register_v1('bobsmith1@gmail.com','2345678','Bobbo','Smith')
    user_id_1 = user1['auth_user_id']

    test_channel = channels_create_v1(user_id, "correct", True)
    channel_id = test_channel['channel_id']

    test_channel_1 = channels_create_v1(user_id_1, "correct", True)

    message_send_v1(user_id, channel_id, "Hello")

    result = search_v1(user_id, "Hello")
    assert len(result) == 1

@clear 
def test_many_matches():

    user = auth_register_v1('bobsmith2@gmail.com','12345678','Bob','Smith')
    user_id = user['auth_user_id']

    test_channel = channels_create_v1(user_id, "test channel", True)
    channel_id = test_channel['channel_id']

    message_send_v1(user_id, channel_id, "Hello")
    message_send_v1(user_id, channel_id, "Hello")
    message_send_v1(user_id, channel_id, "Hello")
    message_send_v1(user_id, channel_id, "Hello")
    message_send_v1(user_id, channel_id, "Hello")

    result = search_v1(user_id, "Hello")
    assert len(result) == 5
