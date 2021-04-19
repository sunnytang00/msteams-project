import pytest

from src.notifications import get_notifications, notifactions_get_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1, channels_listall_v1 ,channels_list_v1
from src.message import message_send_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_invite_channel(helper):
    invitor_user_id = helper.register_user(1, name_first='bob', name_last='smith')
    invitee_user_id = helper.register_user(2)

    channel = channels_create_v1(invitor_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    channel_invite_v1(auth_user_id=invitor_user_id, channel_id=channel_id, u_id=invitee_user_id)

    notifications = get_notifications(invitee_user_id)

    assert len(notifications) == 1
    assert notifications[0].get('notification_message') == 'bobsmith added you to Cat Society'

@clear
def test_empty_notifications(helper):
    u_id = helper.register_user(1)

    notifications = notifactions_get_v1(u_id)
    assert len(notifications) == 0

@clear
def test_tag_someone(helper):
    invitor_user_id = helper.register_user(1, name_first='bob', name_last='smith')
    invitee_user_id = helper.register_user(2)

    channel = channels_create_v1(invitor_user_id, "Cat Society", True)
    channel_id = channel['channel_id']

    channel_invite_v1(auth_user_id=invitor_user_id, channel_id=channel_id, u_id=invitee_user_id)
    message = '@bobsmith'
    message_send_v1(invitor_user_id, channel_id, message) 
    message = 'wdqdwdq@bobsmith'
    message_send_v1(invitor_user_id, channel_id, message) 
    message = '@bobsmith @bobsmith @'
    message_send_v1(invitor_user_id, channel_id, message) 
    notifications = notifactions_get_v1(invitor_user_id)
    print(notifications)
    assert notifications[0].get('notification_message') == f'bobsmith tagged you in Cat Society: @bobsmith'

