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
def test_pin_single_message(helper):
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
    