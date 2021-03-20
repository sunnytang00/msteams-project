import hashlib
import jwt

SECRET = 'FRI09BECHO'

def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

#Takes in 2 strings, first name and last name, concatenates them and jwts it
def encode_jwt(firstname: str, lastname: str)  -> str:

    ret = firstname.lower() + lastname.lower()
    return jwt.encode(ret, SECRET, algorithm='HS256')

#takes in a jwt and decodes it
def decode_jwt(jwt: str) -> str:
    return jwt.decode(jwt, SECRET, algorithms='HS256')
