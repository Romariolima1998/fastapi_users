from pwdlib import PasswordHash

pwdhash = PasswordHash.recommended()

def hash(password:str) -> str:
    return pwdhash.hash(password)

def verify(password: str, password_hash: str) -> bool:
    return pwdhash.verify(password, password_hash)