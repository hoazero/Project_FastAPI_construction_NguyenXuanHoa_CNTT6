from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.site import SiteMember, SiteRole
from app.models.user import User
from app.services.site_service import (
    get_site_by_id,
    get_site_member,
)


def get_site_member_or_403(
    site_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    site = get_site_by_id(
        db=db,
        site_id=site_id,
    )

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công trình",
        )

    member = get_site_member(
        db=db,
        site_id=site_id,
        user_id=current_user.id,
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải là thành viên của công trình này",
        )

    return member


def require_site_owner(
    site_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    site = get_site_by_id(
        db=db,
        site_id=site_id,
    )

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công trình",
        )

    member = get_site_member(
        db=db,
        site_id=site_id,
        user_id=current_user.id,
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải là thành viên của công trình này",
        )

    if member.role != SiteRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ chủ công trình mới được phép thực hiện thao tác này",
        )

    return member