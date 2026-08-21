from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WorkItemBase(BaseModel):
    title: str
    description: str | None = None
    assignee_id: int | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: datetime | None = None


class WorkItemCreate(WorkItemBase):
    pass


class WorkItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None


class WorkItemResponse(WorkItemBase):
    id: int
    site_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )