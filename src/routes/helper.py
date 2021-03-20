import hashlib
import jwt
from uuid import uuid4

SECRET = 'FRI09BECHO'

def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def encode_token(session_id: str)  -> str:
    """Takes in 2 strings, first name and last name, concatenates them and jwts it"""
    payload = {'session_id': session_id}
    return jwt.encode(payload, SECRET, algorithm='HS256')

def decode_token(payload: str) -> str:
    """takes in a jwt and decodes it"""
    return jwt.decode(payload, SECRET, algorithms='HS256')

def get_new_session_id():
    return str(uuid4())