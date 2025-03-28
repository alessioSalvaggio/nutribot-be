import hashlib
import os

def check_password(password: str, saved_hash: str) -> bool:
    salt, stored_hash = saved_hash.split(":")
    salt = bytes.fromhex(salt)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hashed.hex() == stored_hash

def hash_password(password: str) -> str:
    salt = os.urandom(16) 
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + ":" + hashed.hex() 
