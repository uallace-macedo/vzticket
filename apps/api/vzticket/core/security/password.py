from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()


def generate_hash(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return _password_hash.verify(password, hash)
