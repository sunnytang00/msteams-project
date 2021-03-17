import hashlib
import jwt

def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

#Takes in 2 strings, first name and last name, concatenates them and jwts it
#if handle is taken
def encode_jwt(firstname: str, lastname: str, num: int or None) -> str:
    if num != None:
        ret = firstname.lower() + lastname.lower() + num
    else:
        ret = firstname.lower() + lastname.lower()
    return jwt.encode(ret, "FRI09BECHO", algorithm='HS256')

#takes in a jwt and decodes it
def decode_jwt(jwt: str) -> str:
    return jwt.decode(jwt, "FRI09BECHO", algorithms='HS256')
