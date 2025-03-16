import unicodedata

from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(plain_password: str):
    normalized_plain_password = unicodedata.normalize("NFC", plain_password)

    return password_context.hash(normalized_plain_password)


def verify_password(plain_password: str, hashed_password: str):
    normalized_plain_password = unicodedata.normalize("NFC", plain_password)
    normalized_hashed_password = unicodedata.normalize("NFC", hashed_password)

    return password_context.verify(normalized_plain_password, normalized_hashed_password)
