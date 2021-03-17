import hashlib
import jtw

def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

#Takes in 2 strings, first name and last name, concatenates them and jwts it
def encode_jwt(firstname: str, lastname: str)  -> str:
    ret = lower(firstname) + lower(lastname)
    return jwt.encode(ret, "FRI09BECHO", algorithms='HS256')
#takes in a jwt and decodes it
def decode_jwt(jwt: str) -> str:
    return jwt.decode(jwt, "FRI09BECHO", algorithms='HS256')
