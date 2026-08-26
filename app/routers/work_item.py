from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    status,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.permissions import (
    get_site_member_or_403,
    get_work_item_owner_or_403,
    get_work_item_with_member,
)
from app.models.site import SiteMember, SiteRole
from app.models.user import User
from app.models.work_item import WorkItem

from app.schemas.work_item import (
    WorkItemCreate,
    WorkItemResponse,
    WorkItemUpdate,
    WorkItemPriority,
    WorkItemStatus,
)
from app.services.site_service import (
    get_site_member,
)
from app.services.work_item_service import (
    create_work_item,
    delete_work_item,
    get_work_items,
    update_work_item,
)
from app.utils.response import (
    success_response,
)

router = APIRouter(
    tags=["Work Items"]
)

@router.post(
    "/construction-sites/{site_id}/work-items",
    status_code=status.HTTP_201_CREATED,
)
def create_work_item_api(
    site_id: int,
    data: WorkItemCreate,
    request: Request,
    member: SiteMember = Depends(
        get_site_member_or_403
    ),
    db: Session = Depends(get_db),
):
    work_item = create_work_item(
        db=db,
        site_id=site_id,
        data=data,
    )

    response_data = (
        WorkItemResponse.model_validate(
            work_item
        ).model_dump(mode="json")
    )

    return success_response(
        request=request,
        data=response_data,
        message="Tạo hạng mục thi công thành công",
        status_code=status.HTTP_201_CREATED,
    )

@router.get(
    "/construction-sites/{site_id}/work-items",
)
def list_work_items_api(
    site_id: int,
    request: Request,

    status_filter: WorkItemStatus | None = Query(
        None,
        alias="status",
    ),

    priority: WorkItemPriority | None = None,

    assignee_id: int | None = Query(
        None,
        ge=1,
    ),

    search: str | None = None,

    limit: int = Query(
        20,
        ge=1,
        le=100,
    ),

    offset: int = Query(
        0,
        ge=0,
    ),

    sort_by: str = Query(
        "created_at",
        pattern="^(created_at|due_date)$",
    ),

    member: SiteMember = Depends(
        get_site_member_or_403
    ),

    db: Session = Depends(get_db),
):
    items = get_work_items(
        db=db,
        site_id=site_id,
        status=status_filter,
        priority=priority,
        assignee_id=assignee_id,
        search=search,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
    )

    data = [
        WorkItemResponse.model_validate(
            item
        ).model_dump(mode="json")
        for item in items
    ]

    return success_response(
        request=request,
        data=data,
        message=(
            "Lấy danh sách hạng mục "
            "thi công thành công"
        ),
    )

@router.get(
    "/work-items/{item_id}",
)
def get_work_item_api(
    item_id: int,
    request: Request,

    result=Depends(
        get_work_item_with_member
    ),
):
    work_item, member, current_user = result

    response_data = (
        WorkItemResponse.model_validate(
            work_item
        ).model_dump(mode="json")
    )

    return success_response(
        request=request,
        data=response_data,
        message=(
            "Lấy chi tiết hạng mục "
            "thi công thành công"
        ),
    )

@router.patch(
    "/work-items/{item_id}",
)
def update_work_item_api(
    item_id: int,
    data: WorkItemUpdate,
    request: Request,

    result=Depends(
        get_work_item_with_member
    ),

    db: Session = Depends(get_db),
):
    work_item, member, current_user = result

    update_data = data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không có dữ liệu để cập nhật",
        )

    # ==========================
    # OWNER
    # ==========================

    if member.role == SiteRole.OWNER:

        # Owner có toàn quyền
        pass

    # ==========================
    # ASSIGNEE
    # ==========================

    elif (work_item.assignee_id == current_user.id):

        # Assignee chỉ được đổi status
        if set(update_data) != {"status"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Người được giao chỉ được "
                    "cập nhật trạng thái"
                ),
            )

    # ==========================
    # MEMBER
    # ==========================

    elif member.role == SiteRole.MEMBER:

        # Member không được giao việc
        if "assignee_id" in update_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Thành viên không có quyền "
                    "giao việc"
                ),
            )

        # Member không được đổi status
        if "status" in update_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Thành viên không có quyền "
                    "cập nhật trạng thái"
                ),
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền thực hiện thao tác này",
        )

    # ==========================
    # VALIDATE ASSIGNEE
    # ==========================

    if "assignee_id" in update_data:

        assignee_id = update_data["assignee_id"]

        if assignee_id is not None:

            assignee_member = get_site_member(
                db=db,
                site_id=work_item.site_id,
                user_id=assignee_id,
            )

            if not assignee_member:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "Người được giao không "
                        "thuộc công trình này"
                    ),
                )

    work_item = update_work_item(
        db=db,
        work_item=work_item,
        data=data,
    )

    response_data = (
        WorkItemResponse.model_validate(
            work_item
        ).model_dump(mode="json")
    )

    return success_response(
        request=request,
        data=response_data,
        message=(
            "Cập nhật hạng mục thi công "
            "thành công"
        ),
    )

@router.delete(
    "/work-items/{item_id}",
)
def delete_work_item_api(
    item_id: int,
    request: Request,

    work_item=Depends(
        get_work_item_owner_or_403
    ),

    db: Session = Depends(get_db),
):
    delete_work_item(
        db=db,
        work_item=work_item,
    )

    return success_response(
        request=request,
        data=None,
        message="Xóa hạng mục thi công thành công",
    )