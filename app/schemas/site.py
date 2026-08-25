from datetime import datetime
# from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SiteBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class SiteCreate(SiteBase):
    pass


class SiteUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
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
    # role: Literal["MEMBER"] = "MEMBER"


class SiteMemberResponse(BaseModel):
    site_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )