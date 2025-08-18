from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(plain_password: str) -> str:
    if not plain_password:
        raise ValueError("Password cannot be empty.")
    return pwd_context.hash(plain_password)


def authenticate_user(
    plain_password: str, hashed_password: str
) -> tuple[bool, str | None]:
    if not pwd_context.verify(plain_password, hashed_password):
        return False, None

    if pwd_context.needs_update(hashed_password):
        new_hash = pwd_context.hash(plain_password)
        return True, new_hash

    return True, None
