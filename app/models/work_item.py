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

class WorkItem(Base):
    __tablename__ = "work_items"
    id = Column(Integer,primary_key=True,index=True)
    site_id = Column(Integer,ForeignKey("construction_sites.id"),nullable=False)
    title = Column(String(255),nullable=False)
    description = Column(Text,nullable=True)
    assignee_id = Column(Integer,ForeignKey("users.id"),nullable=True)
    status = Column(Enum("TODO","IN_PROGRESS","DONE"),default="TODO",nullable=False)
    priority = Column(Enum("LOW","MEDIUM","HIGH"),default="MEDIUM",nullable=False)
    due_date = Column(DateTime,nullable=True)
    created_at = Column(DateTime,default=datetime.now,nullable=False)

    site = relationship(
        "ConstructionSite",
        back_populates="work_items"
    )

    assignee = relationship(
        "User",
        back_populates="assigned_work_items"
    )