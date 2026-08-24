from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import (
    get_current_user,
    require_admin,
)
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import get_users


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_all_users(
    search: str | None = None,
    is_active: bool | None = None,
    admin_user: User = Depends(
        require_admin
    ),
    db: Session = Depends(get_db)
):

    return get_users(
        db=db,
        search=search,
        is_active=is_active
    )