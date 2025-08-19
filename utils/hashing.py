from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash(plain: str) -> str:
    if not plain:
        raise ValueError("Password cannot be empty.")
    return pwd_context.hash(plain)


def verify_hash(plain: str, hash: str) -> bool:
    if not plain:
        raise ValueError("Invalid hashing argument")
    if not hash:
        raise ValueError("Invalid hashing argument")
    return pwd_context.verify(plain, hash)


def authenticate_user(
    plain_password: str, hashed_password: str
) -> tuple[bool, str | None]:
    if not pwd_context.verify(plain_password, hashed_password):
        return False, None

    if pwd_context.needs_update(hashed_password):
        new_hash = pwd_context.hash(plain_password)
        return True, new_hash

    return True, None
