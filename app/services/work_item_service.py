from sqlalchemy.orm import Session

from app.models.work_item import WorkItem
from app.schemas.work_item import (
    WorkItemCreate,
    WorkItemUpdate,
)


def create_work_item(
    db: Session,
    site_id: int,
    data: WorkItemCreate,
):
    work_item = WorkItem(
        site_id=site_id,
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        priority=data.priority.value,
        status="TODO",
    )

    db.add(work_item)
    db.commit()
    db.refresh(work_item)

    return work_item


def get_work_item(
    db: Session,
    item_id: int,
):
    return (
        db.query(WorkItem)
        .filter(
            WorkItem.id == item_id
        )
        .first()
    )


def get_work_items(
    db: Session,
    site_id: int,
    status=None,
    priority=None,
    assignee_id=None,
    search=None,
    limit=20,
    offset=0,
    sort_by="created_at",
):
    query = (
        db.query(WorkItem)
        .filter(
            WorkItem.site_id == site_id
        )
    )

    if status is not None:
        query = query.filter(
            WorkItem.status == status.value
        )

    if priority is not None:
        query = query.filter(
            WorkItem.priority == priority.value
        )

    if assignee_id is not None:
        query = query.filter(
            WorkItem.assignee_id == assignee_id
        )

    if search:
        query = query.filter(
            WorkItem.title.ilike(
                f"%{search}%"
            )
        )

    if sort_by == "due_date":
        query = query.order_by(
            WorkItem.due_date.asc()
        )
    else:
        query = query.order_by(
            WorkItem.created_at.desc()
        )

    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )


def update_work_item(
    db: Session,
    work_item: WorkItem,
    data: WorkItemUpdate,
):
    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        if hasattr(value, "value"):
            value = value.value

        setattr(
            work_item,
            field,
            value,
        )

    db.commit()
    db.refresh(work_item)

    return work_item


def delete_work_item(
    db: Session,
    work_item: WorkItem,
):
    db.delete(work_item)
    db.commit()