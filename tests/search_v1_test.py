from src.error import InputError, AccessError
from src.message import message_send_v1, message_remove_v1, message_edit_v1
import pytest
from tests.helper import helper, clear
from src.other import search_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1

@clear
def test_empty_query_str(helper):
    user_id = helper.register_user(1)

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
def test_query_too_long(helper):
    user_id = helper.register_user(1)
    with pytest.raises(InputError) as e:
        search_v1(user_id, "F" * 1001)
        assert 'Query string is too long' in str(e)

@clear 
def test_no_match(helper):
    user_id = helper.register_user(1)
    channel_id = helper.create_channel(1, user_id)

    message_send_v1(user_id, channel_id, "Hello")

    assert search_v1(user_id, "Hello1") == []

@clear 
def test_one_match(helper):
    user_id = helper.register_user(1)
    channel_id = helper.create_channel(1, user_id)

    message_send_v1(user_id, channel_id, "Hello")

    result = search_v1(user_id, "Hello")
    assert len(result) == 1

@clear 
def test_not_in_a_channel(helper):

    user_id = helper.register_user(1)

    channel_id = helper.create_channel(1, user_id)

    helper.create_channel(2, user_id)


    message_send_v1(user_id, channel_id, "Hello")

    result = search_v1(user_id, "Hello")
    assert len(result) == 1

@clear 
def test_many_matches(helper):

    user_id = helper.register_user(1)
    channel_id = helper.create_channel(1, user_id)

    message_send_v1(user_id, channel_id, "Hello")
    message_send_v1(user_id, channel_id, "Hello")
    message_send_v1(user_id, channel_id, "Hello")
    message_send_v1(user_id, channel_id, "Hello")
    message_send_v1(user_id, channel_id, "Hello")

    result = search_v1(user_id, "Hello")
    assert len(result) == 5
