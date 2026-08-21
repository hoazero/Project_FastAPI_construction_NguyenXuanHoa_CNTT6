from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SiteBase(BaseModel):
    name: str
    description: str | None = None


class SiteCreate(SiteBase):
    pass


class SiteUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class SiteResponse(SiteBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class SiteMemberCreate(BaseModel):
    user_id: int
    role: str = "MEMBER"


class SiteMemberResponse(BaseModel):
    site_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )