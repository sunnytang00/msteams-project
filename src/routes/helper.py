import hashlib

def hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()