from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import relationship
from app.db.database import Base

class ConstructionSite(Base):
    __tablename__ = "construction_sites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),nullable=False)
    description = Column(Text,nullable=True)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime,default=datetime.now,nullable=False)

    owner = relationship(
        "User",
        back_populates="owned_sites"
    )

    members = relationship(
        "SiteMember",
        back_populates="site",
        cascade="all"
    )

    work_items = relationship(
        "WorkItem",
        back_populates="site",
        cascade="all"
    )


class SiteMember(Base):
    __tablename__ = "site_members"
    site_id = Column(Integer,ForeignKey("construction_sites.id"),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),primary_key=True)
    role = Column(Enum("OWNER", "MEMBER"),nullable=False)
    joined_at = Column(DateTime,default=datetime.now,nullable=False)

    site = relationship(
        "ConstructionSite",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="site_members"
    )