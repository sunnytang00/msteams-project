import pytest

from src.base.notifications import get_notifications
from src.base.channel import channel_invite_v1
from src.base.channels import channels_create_v1, channels_listall_v1 ,channels_list_v1
from src.base.error import InputError, AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
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