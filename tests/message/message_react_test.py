import pytest
from src.base.message import message_send_v1, message_senddm_v1, message_remove_v1, message_edit_v1, message_react_v1
from src.base.auth import auth_register_v1
from src.base.dm import dm_create_v1, dm_messages_v1, dm_invite_v1
from src.base.channel import channel_messages_v1, channel_invite_v1, channel_join_v1, channel_addowner_v1
from src.base.other import clear_v1
from src.base.error import InputError, AccessError
from tests.helper import helper, clear
from src.base.channels import channels_create_v1
from src.base.helper import is_pinned, get_channel, get_react_uids

valid_react_id = 1
invalid_react_id = 2
@clear
def test_react_single_message_channel(helper):
    """Add two messages and pin the second one"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2
    channel_id = channels_create_v1(auth_user_id1, "message_test", True).get('channel_id')
    assert channel_id == 1
    channel_invite_v1(auth_user_id1, channel_id, auth_user_id2)

    first_message = "this shouldnt have reacts"
    second_message = "hopefully this one does"

    message_info1 = message_send_v1(auth_user_id1, channel_id, first_message)
    message_id1 = message_info1.get('message_id')
    assert message_id1 == 1

    message_info2 = message_send_v1(auth_user_id1, channel_id, second_message)
    message_id2 = message_info2.get('message_id')
    assert message_id2 == 2

    message_react_v1(auth_user_id1, message_id2, valid_react_id)

    assert get_react_uids(message_id2) == [1]

    message_react_v1(auth_user_id2, message_id2, valid_react_id)

    assert get_react_uids(message_id2) == [1,2]

@clear
def test_react_single_message_dm(helper):
    """Add two messages and pin the second one"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2
    dm_id = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    assert dm_id == 1

    first_message = "this shouldnt have reacts"
    second_message = "hopefully this one does"

    message_info1 = message_senddm_v1(auth_user_id1, dm_id, first_message)
    message_id1 = message_info1.get('message_id')
    assert message_id1 == 1

    message_info2 = message_senddm_v1(auth_user_id1, dm_id, second_message)
    message_id2 = message_info2.get('message_id')
    assert message_id2 == 2

    message_react_v1(auth_user_id1, message_id2, valid_react_id)

    assert get_react_uids(message_id2) == [1]

    message_react_v1(auth_user_id2, message_id2, valid_react_id)

    assert get_react_uids(message_id2) == [1,2]

@clear
def test_invalid_react_id(helper):
    """Add two messages and pin the second one"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2

    channel_id = channels_create_v1(auth_user_id1, "message_test", True).get('channel_id')
    assert channel_id == 1
    channel_invite_v1(auth_user_id1, channel_id, auth_user_id2)

    dm_id = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    assert dm_id == 1

    first_message = "this shouldnt have reacts"
    second_message = "hopefully this one does"

    message_info1 = message_senddm_v1(auth_user_id1, dm_id, first_message)
    message_id1 = message_info1.get('message_id')
    assert message_id1 == 1

    message_info2 = message_senddm_v1(auth_user_id1, dm_id, second_message)
    message_id2 = message_info2.get('message_id')
    assert message_id2 == 2

    message_info3 = message_send_v1(auth_user_id1, channel_id, first_message)
    message_id3 = message_info3.get('message_id')
    assert message_id3 == 3

    message_info4 = message_send_v1(auth_user_id1, channel_id, second_message)
    message_id4 = message_info4.get('message_id')
    assert message_id4 == 4

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id1, message_id1, invalid_react_id)
        assert f'react_id {invalid_react_id} is not a valid React ID' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id1, message_id2, invalid_react_id)
        assert f'react_id {invalid_react_id} is not a valid React ID' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id2, message_id1, invalid_react_id)
        assert f'react_id {invalid_react_id} is not a valid React ID' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id2, message_id2, invalid_react_id)
        assert f'react_id {invalid_react_id} is not a valid React ID' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id1, message_id3, invalid_react_id)
        assert f'react_id {invalid_react_id} is not a valid React ID' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id1, message_id4, invalid_react_id)
        assert f'react_id {invalid_react_id} is not a valid React ID' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id2, message_id3, invalid_react_id)
        assert f'react_id {invalid_react_id} is not a valid React ID' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id2, message_id4, invalid_react_id)
        assert f'react_id {invalid_react_id} is not a valid React ID' in str(e.value)

    assert get_react_uids(message_id1) == []
    assert get_react_uids(message_id2) == []
    assert get_react_uids(message_id3) == []
    assert get_react_uids(message_id4) == []


@clear
def test_react_to_invalid_msg_id(helper):
    """Add two messages and pin the second one"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2

    channel_id = channels_create_v1(auth_user_id1, "message_test", True).get('channel_id')
    assert channel_id == 1
    channel_invite_v1(auth_user_id1, channel_id, auth_user_id2)

    dm_id = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    assert dm_id == 1

    invalid_message_id = 33
    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id1, invalid_message_id, valid_react_id)
        assert f'message_id {invalid_message_id} is not a valid message within a channel/dm' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id2, invalid_message_id, valid_react_id)
        assert f'message_id {invalid_message_id} is not a valid message within a channel/dm' in str(e.value)

@clear
def test_non_member_react_and_react_reacted(helper):
    """Add two messages and pin the second one"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    auth_user_id3 = helper.register_user(3)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2
    assert auth_user_id3 == 3

    channel_id = channels_create_v1(auth_user_id1, "message_test", True).get('channel_id')
    assert channel_id == 1
    channel_invite_v1(auth_user_id1, channel_id, auth_user_id2)

    dm_id = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    assert dm_id == 1

    first_message = "this shouldnt have reacts"

    message_info1 = message_senddm_v1(auth_user_id1, dm_id, first_message)
    message_id1 = message_info1.get('message_id')
    assert message_id1 == 1

    message_info2 = message_send_v1(auth_user_id1, channel_id, first_message)
    message_id2 = message_info2.get('message_id')
    assert message_id2 == 2
    
    with pytest.raises(AccessError) as e: 
        message_react_v1(auth_user_id3, message_id1, valid_react_id)
        assert f'member with id {auth_user_id3} is not dm member' in str(e.value)

    assert get_react_uids(message_id1) == []

    dm_invite_v1(auth_user_id2, dm_id, auth_user_id3)
    message_react_v1(auth_user_id3, message_id1, valid_react_id)

    assert get_react_uids(message_id1) == [3]
    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id3, message_id1, valid_react_id)
        assert f'user with id {auth_user_id3} has already reacted to message id {message_id1} in dm' in str(e.value)

    with pytest.raises(AccessError) as e: 
        message_react_v1(auth_user_id3, message_id2, valid_react_id)
        assert f'member with id {auth_user_id3} is not channel member' in str(e.value)

    channel_invite_v1(auth_user_id2, channel_id, auth_user_id3)
    message_react_v1(auth_user_id3, message_id2, valid_react_id)

    assert get_react_uids(message_id2) == [3]

    with pytest.raises(InputError) as e: 
        message_react_v1(auth_user_id3, message_id2, valid_react_id)
        assert f'user with id {auth_user_id3} has already reacted to message id {message_id2} in channel' in str(e.value)

