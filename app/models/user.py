from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String
)
from sqlalchemy.orm import relationship
from app.db.database import Base
from enum import Enum as Enum2

class UserRole(str, Enum2):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(255),unique=True,nullable=False,index=True)
    password_hash = Column(String(255),nullable=False)
    full_name = Column(String(255),nullable=False)
    role = Column(Enum("USER", "ADMIN"),default="USER",nullable=False)
    is_active = Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime,default=datetime.now,nullable=False)

    owned_sites = relationship(
        "ConstructionSite",
        back_populates="owner"
    )

    site_members = relationship(
        "SiteMember",
        back_populates="user",
        cascade="all"
    )

    assigned_work_items = relationship(
        "WorkItem",
        back_populates="assignee"
    )