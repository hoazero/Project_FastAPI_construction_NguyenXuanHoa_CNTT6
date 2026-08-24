from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_id(
    db: Session,
    user_id: int
) -> User | None:

    return db.query(User).filter(
        User.id == user_id
    ).first()


def get_user_by_email(
    db: Session,
    email: str
) -> User | None:

    return db.query(User).filter(
        User.email == email
    ).first()


def get_users(
    db: Session,
    search: str | None = None,
    is_active: bool | None = None
) -> list[User]:

    query = db.query(User)

    if search:
        keyword = f"%{search}%"

        query = query.filter(
            or_(
                User.full_name.ilike(keyword),
                User.email.ilike(keyword)
            )
        )

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    query = query.order_by(User.id)

    return query.all()