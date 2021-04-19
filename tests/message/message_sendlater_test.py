import pytest
from src.message import message_sendlater_v1
from src.channel import channel_messages_v1
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from tests.helper import helper, clear
from src.channels import channels_create_v1
import time
@clear
def test_valid_input(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msg = "1234"
    time_sent = int(time.time()) + 1
    message_id = message_sendlater_v1(auth_user_id, ch_id, msg, time_sent)
    time.sleep(2)
    
    msgs = channel_messages_v1(auth_user_id, ch_id, 0)

    assert len(msgs.get('messages')) == 1 and msgs.get('messages')[0].get('message') == "1234" and \
        message_id.get('message_id') == msgs.get('messages')[0].get('message_id')

@clear
def test_invalid_channel(helper):
    auth_user_id = helper.register_user(1)
    ch_id = 10 
    msg = "1234"
    time_sent = int(time.time()) + 10
    with pytest.raises(InputError) as e: 
        message_sendlater_v1(auth_user_id, ch_id, msg, time_sent)
        assert f'Channel ID {ch_id} is not a valid channel' in str(e.value)

@clear
def test_msg_too_long(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msg = "1" * 1001
    time_sent = int(time.time()) + 10
    with pytest.raises(InputError) as e: 
        message_sendlater_v1(auth_user_id, ch_id, msg, time_sent)
        assert 'Message is more than 1000 characters' in str(e.value)

@clear
def test_past_time(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msg = "1234"
    time_sent = int(time.time()) - 10
    with pytest.raises(InputError) as e: 
        message_sendlater_v1(auth_user_id, ch_id, msg, time_sent)
        assert 'Time sent is a time in the past' in str(e.value)

@clear
def test_invalid_token(helper):
    auth_user_id = helper.register_user(1)
    ch_id = helper.create_channel(1, auth_user_id)
    msg = "1234"
    time_sent = int(time.time()) + 10
    with pytest.raises(AccessError) as e: 
        message_sendlater_v1(auth_user_id + 10, ch_id, msg, time_sent)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e.value)

@clear
def test_not_member_of_channel(helper):
    auth_user_id = helper.register_user(1)
    u_id = helper.register_user(2)
    ch_id = helper.create_channel(2, u_id)
    msg = "1234"
    time_sent = int(time.time()) + 10
    with pytest.raises(AccessError) as e: 
        message_sendlater_v1(auth_user_id, ch_id, msg, time_sent)
        assert ' the authorised user is not a member of the DM they are trying to post to' in str(e.value)