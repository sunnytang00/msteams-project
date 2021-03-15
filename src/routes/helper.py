import hashlib

def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()