import hashlib
import jwt

SECRET = 'FRI09BECHO'

def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def encode_jwt(firstname: str, lastname: str)  -> str:
    """Takes in 2 strings, first name and last name, concatenates them and jwts it"""

    payload = firstname.lower() + lastname.lower()
    return jwt.encode(payload, SECRET, algorithm='HS256')

def decode_jwt(payload: str) -> str:
    """takes in a jwt and decodes it"""
    return jwt.decode(payload, SECRET, algorithms='HS256')
