import pytest
from src.base.message import message_send_v1, message_remove_v1
from src.base.auth import auth_register_v1
from src.base.channel import channel_messages_v1
from src.base.other import clear_v1
from src.base.error import InputError, AccessError
from tests.helper import helper, clear
from src.base.channels import channels_create_v1

@clear
def test_message_remove_single():
    """TODO test sucks """
    user = auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@99',
                        name_first='Harry',
                        name_last='Potter')

    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1

    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')
    assert channel_id == 1

    message_info = message_send_v1(auth_user_id, channel_id, "an epic message")
    message_id = message_info.get('message_id')
    assert message_info.get('message_id') == 1

    start_and_end_keys = 2
    assert len(channel_messages_v1(auth_user_id, channel_id, 1)) - start_and_end_keys == 1

    message_remove_v1(auth_register_v1, message_id)
