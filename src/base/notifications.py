"""TODO"""
from src.base.helper import get_notifications

def notifactions_get_v1(auth_user_id):
    """TODO"""
    return get_notifications(auth_user_id)[-20:]
