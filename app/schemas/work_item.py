from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

class WorkItemStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class WorkItemPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class WorkItemBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255
    )
    description: str | None = None
    assignee_id: int | None = None
    status: WorkItemStatus = (WorkItemStatus.TODO)
    priority: WorkItemPriority = (WorkItemPriority.MEDIUM)
    due_date: datetime | None = None


class WorkItemCreate(WorkItemBase):
    title: str = Field(
        min_length=1,
        max_length=255
    )
    description: str | None = None
    due_date: datetime | None = None
    priority: WorkItemPriority = (WorkItemPriority.MEDIUM)


class WorkItemUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )
    description: str | None = None
    assignee_id: int | None = None
    status: WorkItemStatus = (WorkItemStatus.TODO)
    priority: WorkItemPriority = (WorkItemPriority.MEDIUM)
    due_date: datetime | None = None


class WorkItemResponse(WorkItemBase):
    id: int
    site_id: int
    title: str
    description: str | None
    assignee_id: int | None
    status: WorkItemStatus
    priority: WorkItemPriority
    due_date: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )