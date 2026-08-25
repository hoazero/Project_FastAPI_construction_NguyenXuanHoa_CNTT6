from fastapi import (
    APIRouter,
    Depends,
    Query,
    Request,
    status,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import (
    get_site_member_or_403,
    require_site_owner,
)
from app.models.user import User
from app.models.site import SiteRole
from app.schemas.site import (
    SiteCreate,
    SiteResponse,
    SiteUpdate,
    SiteMemberCreate,
    SiteMemberResponse
)
from app.services.site_service import (
    add_site_member,
    create_site,
    delete_site,
    delete_site_member,
    get_site_by_id,
    get_site_member,
    get_site_members,
    get_user_sites,
    update_site
)
from app.utils.response import (
    error_response,
    success_response,
)


router = APIRouter(
    prefix="/construction-sites",
    tags=["Construction Sites"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_construction_site(
    site_data: SiteCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not site_data.name.strip():
        return error_response(
            request=request,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Tên công trình không được để trống",
        )

    site = create_site(
        db=db,
        site_data=site_data,
        current_user_id=current_user.id,
    )

    site_response = SiteResponse.model_validate(site)

    return success_response(
        request=request,
        data=site_response.model_dump(),
        message="Tạo công trình thành công",
        status_code=status.HTTP_201_CREATED,
    )


@router.get("")
def list_construction_sites(
    request: Request,
    search: str | None = Query(
        default=None,
        description="Tìm kiếm công trình theo tên",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sites = get_user_sites(
        db=db,
        current_user_id=current_user.id,
        search=search,
    )

    site_responses = [
        SiteResponse.model_validate(site).model_dump()
        for site in sites
    ]

    return success_response(
        request=request,
        data=site_responses,
        message="Lấy danh sách công trình thành công",
    )

@router.post("/{site_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(
    site_id: int,
    member_data: SiteMemberCreate,
    request: Request,
    owner=Depends(require_site_owner),
    db: Session = Depends(get_db),
):
    # Kiểm tra user đã là member của công trình chưa
    existing_member = get_site_member(
        db=db,
        site_id=site_id,
        user_id=member_data.user_id,
    )

    if existing_member:
        return error_response(
            request=request,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Người dùng đã là thành viên của công trình",
        )

    member = add_site_member(
        db=db,
        site_id=site_id,
        user_id=member_data.user_id,
    )

    member_response = SiteMemberResponse.model_validate(
        member
    )

    return success_response(
        request=request,
        data=member_response.model_dump(),
        message="Thêm thành viên thành công",
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/{site_id}/members")
def list_site_members(
    site_id: int,
    request: Request,
    member=Depends(get_site_member_or_403),
    db: Session = Depends(get_db),
):
    members = get_site_members(
        db=db,
        site_id=site_id,
    )

    member_responses = [
        SiteMemberResponse.model_validate(
            item
        ).model_dump()
        for item in members
    ]

    return success_response(
        request=request,
        data=member_responses,
        message="Lấy danh sách thành viên thành công",
    )


@router.delete("/{site_id}/members/{user_id}")
def remove_site_member(
    site_id: int,
    user_id: int,
    request: Request,
    owner=Depends(require_site_owner),
    db: Session = Depends(get_db),
):
    member = get_site_member(
        db=db,
        site_id=site_id,
        user_id=user_id,
    )

    if not member:
        return error_response(
            request=request,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Thành viên không tồn tại trong công trình",
        )

    # Không cho phép xóa owner
    if member.role == SiteRole.OWNER:
        return error_response(
            request=request,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Không thể xóa owner của công trình",
        )

    delete_site_member(
        db=db,
        member=member,
    )

    return success_response(
        request=request,
        data=None,
        message="Xóa thành viên thành công",
    )

@router.get("/{site_id}")
def get_construction_site(
    site_id: int,
    request: Request,
    member=Depends(get_site_member_or_403),
):
    site_response = SiteResponse.model_validate(
        member.site
    )

    return success_response(
        request=request,
        data=site_response.model_dump(),
        message="Lấy thông tin công trình thành công",
    )


@router.put("/{site_id}")
def update_construction_site(
    site_id: int,
    site_data: SiteUpdate,
    request: Request,
    owner=Depends(require_site_owner),
    db: Session = Depends(get_db),
):

    if site_data.name is not None:
        if not site_data.name.strip():
            return error_response(
                request=request,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Tên công trình không được để trống",
            )

    site = owner.site

    site = update_site(
        db=db,
        site=site,
        site_data=site_data,
    )

    site_response = SiteResponse.model_validate(site)

    return success_response(
        request=request,
        data=site_response.model_dump(),
        message="Cập nhật công trình thành công",
    )


@router.delete("/{site_id}")
def delete_construction_site(
    site_id: int,
    request: Request,
    owner=Depends(require_site_owner),
    db: Session = Depends(get_db),
):
    site = owner.site

    delete_site(
        db=db,
        site=site,
    )

    return success_response(
        request=request,
        data=None,
        message="Xóa công trình thành công",
    )