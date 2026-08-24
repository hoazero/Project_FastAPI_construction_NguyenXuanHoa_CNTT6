from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest
from app.services.user_service import get_user_by_email


def register_user(
    db: Session,
    data: RegisterRequest
) -> User:

    existing_user = get_user_by_email(
        db,
        data.email
    )

    if existing_user:
        raise ValueError(
            "Email đã được sử dụng"
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name.strip(),
        role=UserRole.USER,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User | None:

    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user


def generate_tokens(user: User) -> dict:

    return {
        "access_token": create_access_token(
            user.id
        ),
        "refresh_token": create_refresh_token(
            user.id
        ),
        "token_type": "bearer"
    }