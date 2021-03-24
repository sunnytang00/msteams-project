import requests
from src.config import url

def clear(func):
    """Resets the internal data of the application to it's initial state before running function"""
    def wrapper(*args, **kwargs):
        requests.delete(url + '/clear/v1', json={})
        rv = func(*args, **kwargs)
        return rv
    return wrapper
