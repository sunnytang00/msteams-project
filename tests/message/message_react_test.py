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

@clear
def test_pin_single_message_channel(helper):
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

    message_react_v1(auth_user_id1, message_id2, 1)

    assert get_react_uids(message_id2) == [1]

    message_react_v1(auth_user_id2, message_id2, 1)

    assert get_react_uids(message_id2) == [1,2]

