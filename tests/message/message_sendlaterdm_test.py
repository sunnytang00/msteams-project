import pytest
from src.base.message import message_sendlaterdm_v1
from src.base.dm import dm_messages_v1
from src.base.auth import auth_login_v1, auth_register_v1
from src.base.other import clear_v1
from src.base.error import InputError, AccessError
from tests.helper import helper, clear
from src.base.channels import channels_create_v1
import time

@clear
def test_valid_input(helper):
    auth_user_id = helper.register_user(1)
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')
    msg = "1234"
    time_sent = int(time.time()) + 2
    message_sendlaterdm_v1(auth_user_id, dm_id, msg, time_sent)
    time.sleep(3)
    
    msgs = dm_messages_v1(auth_user_id, dm_id, 0)
    print(msgs.get('messages'))
    assert len(msgs.get('messages')) == 1 and msgs.get('messages')[0].get('message') == "1234"

@clear
def test_invalid_dm(helper):
    auth_user_id = helper.register_user(1)
    dm_id = 10 
    msg = "1234"
    time_sent = int(time.time()) + 10
    with pytest.raises(InputError) as e: 
        message_sendlaterdm_v1(auth_user_id, dm_id, msg, time_sent)
        assert f'DM ID {dm_id} is not a valid DM' in str(e.value)

@clear
def test_msg_too_long(helper):
    auth_user_id = helper.register_user(1)
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')
    msg = "1" * 1001
    time_sent = int(time.time()) + 10
    with pytest.raises(InputError) as e: 
        message_sendlaterdm_v1(auth_user_id, dm_id, msg, time_sent)
        assert 'Message is more than 1000 characters' in str(e.value)

@clear
def test_past_time(helper):
    auth_user_id = helper.register_user(1)
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')
    msg = "1234"
    time_sent = int(time.time()) - 10
    with pytest.raises(InputError) as e: 
        message_sendlaterdm_v1(auth_user_id, dm_id, msg, time_sent)
        assert 'Time sent is a time in the past' in str(e.value)

@clear
def test_invalid_token(helper):
    auth_user_id = helper.register_user(1)
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')
    msg = "1234"
    time_sent = int(time.time()) + 10
    with pytest.raises(AccessError) as e: 
        message_sendlaterdm_v1(auth_user_id + 10, dm_id, msg, time_sent)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e.value)

@clear
def test_not_member_of_DM(helper):
    auth_user_id = helper.register_user(1)
    u_id = helper.register_user(2)
    dm_id = dm_create_v1(u_id, []).get('dm_id')
    msg = "1234"
    time_sent = int(time.time()) + 10
    with pytest.raises(AccessError) as e: 
        message_sendlaterdm_v1(auth_user_id, dm_id, msg, time_sent)
        assert ' the authorised user is not a member of the DM they are trying to post to' in str(e.value)