import pytest
from src.base.message import message_send_v1
from src.base.auth import auth_login_v1, auth_register_v1
from src.base.other import clear_v1
from src.base.error import InputError
from tests.helper import helper, clear
from src.base.channels import channels_create_v1
@clear
def test_message_send_success():

    user = auth_register_v1(email='harrypotter@gmail.com',
                        password='qw3rtyAppl3s@99',
                        name_first='Harry',
                        name_last='Potter')

    auth_user_id = user['auth_user_id']

    channel_id = channels_create_v1(auth_user_id, "message_test", True).get('channel_id')

    assert auth_user_id == 1
    assert channel_id == 1

    message_info = message_send_v1(auth_user_id, channel_id, "hello i hope this works")

    assert message_info.get('message_id') == 1

