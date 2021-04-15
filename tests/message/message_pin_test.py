"""Update a channel or DM message"""

import pytest
from src.base.message import message_send_v1, message_senddm_v1, message_remove_v1, message_edit_v1, message_pin_v1
from src.base.auth import auth_register_v1
from src.base.dm import dm_create_v1, dm_messages_v1
from src.base.channel import channel_messages_v1
from src.base.other import clear_v1
from src.base.error import InputError, AccessError
from tests.helper import helper, clear
from src.base.channels import channels_create_v1
from src.base.helper import is_pinned

@clear
def test_pin_single_message_channel(helper):
    """Add two messages and pin the second one"""
    auth_user_id = helper.register_user(1)
    assert auth_user_id == 1
    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    first_message = "this shouldnt be pinned"
    second_message = "hopefully this one gets pinned"

    message_info = message_send_v1(auth_user_id, channel_id, first_message)
    message_id = message_info.get('message_id')
    assert message_id == 1

    message_info1 = message_send_v1(auth_user_id, channel_id, second_message)
    message_id1 = message_info1.get('message_id')
    assert message_id1 == 2
    message_pin_v1(auth_user_id, message_id1)
    assert is_pinned(message_id) == False
    assert is_pinned(message_id1) == True

@clear
def test_pin_single_message_dm(helper):
    """Add two messages and pin the second one"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2
    
    dm_id = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    assert dm_id == 1

    first_message = "this shouldnt be pinned"
    second_message = "hopefully this one gets pinned"

    message_id1 = message_senddm_v1(auth_user_id2, dm_id, first_message).get('message_id')
    assert message_id1 == 1

    message_id2 = message_senddm_v1(auth_user_id2, dm_id, second_message).get('message_id')
    assert message_id2 == 2

    message_pin_v1(auth_user_id1, message_id2)
    assert is_pinned(message_id1) == False
    assert is_pinned(message_id2) == True

@clear
def test_pin_invalid_message_id(helper):
    """try to pin invalid message id"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2
    
    dm_id = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    assert dm_id == 1

    first_message = "this shouldnt be pinned"
    second_message = "hopefully this one gets pinned"

    message_id1 = message_senddm_v1(auth_user_id2, dm_id, first_message).get('message_id')
    assert message_id1 == 1

    message_id2 = message_senddm_v1(auth_user_id2, dm_id, second_message).get('message_id')
    assert message_id2 == 2

    with pytest.raises(InputError) as e: 
        message_pin_v1(auth_user_id1, 22)
        assert f'message with message id {message_id} is not a valid message' in str(e.value)

@clear
def test__pin_pinned_message(helper):
    """try to pin already pinned message"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2
    
    dm_id = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    assert dm_id == 1

    first_message = "this shouldnt be pinned"
    second_message = "hopefully this one gets pinned"

    message_id1 = message_senddm_v1(auth_user_id2, dm_id, first_message).get('message_id')
    assert message_id1 == 1

    message_id2 = message_senddm_v1(auth_user_id2, dm_id, second_message).get('message_id')
    assert message_id2 == 2

    message_pin_v1(auth_user_id1, message_id2)
    assert is_pinned(message_id1) == False
    assert is_pinned(message_id2) == True
    with pytest.raises(InputError) as e: 
        message_pin_v1(auth_user_id1, message_id2)
        assert f'message with message id {message_id} is already pinned' in str(e.value)
    