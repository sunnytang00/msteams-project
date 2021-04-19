import pytest
from src.message import message_send_v1, message_senddm_v1, message_remove_v1, message_edit_v1, message_pin_v1, message_unpin_v1
from src.auth import auth_register_v1
from src.dm import dm_create_v1, dm_messages_v1, dm_invite_v1
from src.channel import channel_messages_v1, channel_invite_v1, channel_join_v1, channel_addowner_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from tests.helper import helper, clear
from src.channels import channels_create_v1
from src.helper import is_pinned, get_channel

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
    message_unpin_v1(auth_user_id, message_id1)
    assert is_pinned(message_id1) == False

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
    message_unpin_v1(auth_user_id1, message_id2)
    assert is_pinned(message_id1) == False

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

    invalid_msg_id = 22
    with pytest.raises(InputError) as e: 
        message_pin_v1(auth_user_id1, invalid_msg_id)
        assert f'message with message id {invalid_msg_id} is not a valid message' in str(e.value)

    with pytest.raises(InputError) as e: 
        message_unpin_v1(auth_user_id1, invalid_msg_id)
        assert f'message with message id {invalid_msg_id} is not a valid message' in str(e.value)

@clear
def test_pin_pinned_message(helper):
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
        assert f'message with message id {message_id2} is already pinned' in str(e.value)

    message_unpin_v1(auth_user_id1, message_id2)
    assert is_pinned(message_id1) == False
    with pytest.raises(InputError) as e: 
        message_unpin_v1(auth_user_id1, message_id2)
        assert f'message with message id {message_id2} is not pinned' in str(e.value)

@clear
def test_not_channel_member_not_owner(helper):
    """not channel member tries to pin, raises error, then add him, still raises error then finally make him owner"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2
    
    channel_id = channels_create_v1(auth_user_id1, "message_test", True).get('channel_id')
    assert channel_id == 1

    first_message = "this shouldnt be pinned"

    message_info1 = message_send_v1(auth_user_id1, channel_id, first_message)
    message_id1 = message_info1.get('message_id')
    assert message_id1 == 1
    with pytest.raises(AccessError) as e: 
        message_pin_v1(auth_user_id2, message_id1)
        assert f'member with id {auth_user_id2} is not channel member' in str(e.value)

    assert is_pinned(message_id1) == False

    message_pin_v1(auth_user_id1, message_id1)
    assert is_pinned(message_id1) == True
    with pytest.raises(AccessError) as e: 
        message_unpin_v1(auth_user_id2, message_id1)
        assert f'member with id {auth_user_id2} is not channel member' in str(e.value)
    assert is_pinned(message_id1) == True

    message_unpin_v1(auth_user_id1, message_id1)
    assert is_pinned(message_id1) == False

    channel_invite_v1(auth_user_id1, channel_id, auth_user_id2)

    with pytest.raises(AccessError) as e: 
        message_pin_v1(auth_user_id2, message_id1)
        assert f'member with id {auth_user_id2} is not channel owner' in str(e.value)
    
    assert is_pinned(message_id1) == False
    message_pin_v1(auth_user_id1, message_id1)
    assert is_pinned(message_id1) == True

    with pytest.raises(AccessError) as e: 
        message_unpin_v1(auth_user_id2, message_id1)
        assert f'member with id {auth_user_id2} is not channel owner' in str(e.value)

    assert is_pinned(message_id1) == True
    message_unpin_v1(auth_user_id1, message_id1)
    assert is_pinned(message_id1) == False

    channel_addowner_v1(auth_user_id1, channel_id, auth_user_id2)
    message_pin_v1(auth_user_id2, message_id1)
    assert is_pinned(message_id1) == True
    message_unpin_v1(auth_user_id2, message_id1)
    assert is_pinned(message_id1) == False

@clear
def test_not_dm_member_not_owner(helper):
    """not dm member tries to pin, raises error, then add him, still raises error then finally make him owner"""
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    auth_user_id3 = helper.register_user(3)
    assert auth_user_id1 == 1
    assert auth_user_id2 == 2
    assert auth_user_id3 == 3
    
    dm_id = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    assert dm_id == 1

    first_message = "this shouldnt be pinned"

    message_id1 = message_senddm_v1(auth_user_id2, dm_id, first_message).get('message_id')
    assert message_id1 == 1

    with pytest.raises(AccessError) as e: 
        message_pin_v1(auth_user_id3, message_id1)
        assert f'member with id {auth_user_id3} is not dm member' in str(e.value)
    
    assert is_pinned(message_id1) == False
    message_pin_v1(auth_user_id1, message_id1)
    assert is_pinned(message_id1) == True

    with pytest.raises(AccessError) as e: 
        message_unpin_v1(auth_user_id3, message_id1)
        assert f'member with id {auth_user_id3} is not dm member' in str(e.value)

    assert is_pinned(message_id1) == True
    message_unpin_v1(auth_user_id1, message_id1)
    assert is_pinned(message_id1) == False

    dm_invite_v1(auth_user_id1, dm_id, auth_user_id3)

    with pytest.raises(AccessError) as e: 
        message_pin_v1(auth_user_id3, message_id1)
        assert f'member with id {auth_user_id3} is not dm owner' in str(e.value)

    assert is_pinned(message_id1) == False
    message_pin_v1(auth_user_id1, message_id1)
    assert is_pinned(message_id1) == True

    with pytest.raises(AccessError) as e: 
        message_unpin_v1(auth_user_id3, message_id1)
        assert f'member with id {auth_user_id3} is not dm owner' in str(e.value)

    assert is_pinned(message_id1) == True
