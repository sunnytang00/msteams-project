"""TODO"""
from src.helper import get_notifications

def notifactions_get_v1(auth_user_id):
    """TODO"""
    notifications = get_notifications(auth_user_id)[-20:]

    return notifications
