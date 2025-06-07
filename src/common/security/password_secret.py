
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

class PasswordSecret:
    def __init__(self) -> None:
        self.password_hash = PasswordHash((BcryptHasher(),))

    def get_hash_password(self,password: str, salt: bytes | None) -> str:
        return self.password_hash.hash(password, salt=salt)

    def password_verify(self,plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)
    

password_secret: PasswordSecret = PasswordSecret()