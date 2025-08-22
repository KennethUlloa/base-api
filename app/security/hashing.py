from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str | bytes, hashed_password: str | bytes):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str | bytes):
    return pwd_context.hash(password)
