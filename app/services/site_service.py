from sqlalchemy.orm import Session

from app.models.site import (
    ConstructionSite,
    SiteMember,
    SiteRole,
)
from app.schemas.site import SiteCreate, SiteUpdate


def create_site(
    db: Session,
    site_data: SiteCreate,
    current_user_id: int,
):
    site = ConstructionSite(
        name=site_data.name,
        description=site_data.description,
        owner_id=current_user_id,
    )

    db.add(site)
    db.flush()

    owner_member = SiteMember(
        site_id=site.id,
        user_id=current_user_id,
        role=SiteRole.OWNER,
    )

    db.add(owner_member)

    db.commit()
    db.refresh(site)

    return site


def get_user_sites(
    db: Session,
    current_user_id: int,
    search: str | None = None,
):
    query = (
        db.query(ConstructionSite)
        .join(
            SiteMember,
            SiteMember.site_id == ConstructionSite.id,
        )
        .filter(
            SiteMember.user_id == current_user_id
        )
    )

    if search:
        query = query.filter(
            ConstructionSite.name.ilike(f"%{search}%")
        )

    query = query.order_by(
        ConstructionSite.created_at.desc()
    )

    return query.all()


def get_site_by_id(
    db: Session,
    site_id: int,
):
    return (
        db.query(ConstructionSite)
        .filter(
            ConstructionSite.id == site_id
        )
        .first()
    )


def get_site_member(
    db: Session,
    site_id: int,
    user_id: int,
):
    return (
        db.query(SiteMember)
        .filter(
            SiteMember.site_id == site_id,
            SiteMember.user_id == user_id,
        )
        .first()
    )

def add_site_member(
    db: Session,
    site_id: int,
    user_id: int,
):
    member = SiteMember(
        site_id=site_id,
        user_id=user_id,
        role=SiteRole.MEMBER,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member

def get_site_members(
    db: Session,
    site_id: int,
):
    return (
        db.query(SiteMember)
        .filter(
            SiteMember.site_id == site_id
        )
        .order_by(
            SiteMember.joined_at.asc()
        )
        .all()
    )

def delete_site_member(
    db: Session,
    member: SiteMember,
):
    db.delete(member)
    db.commit()

def update_site(
    db: Session,
    site: ConstructionSite,
    site_data: SiteUpdate,
):
    update_data = site_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(site, field, value)

    db.commit()
    db.refresh(site)

    return site


def delete_site(
    db: Session,
    site: ConstructionSite,
):
    db.delete(site)
    db.commit()