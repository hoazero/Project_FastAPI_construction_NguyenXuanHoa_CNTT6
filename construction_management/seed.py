from app.db.database import SessionLocal
from app.core.security import hash_password

from app.models.user import User
from app.models.site import (
    ConstructionSite,
    SiteMember
)
from app.models.work_item import WorkItem


def seed():
    db = SessionLocal()

    try:
        existing_admin = db.query(User).filter(
            User.email == "admin@gmail.com"
        ).first()

        if existing_admin:
            print("Seed data already exists.")
            return


        admin = User(
            email="admin@gmail.com",
            password_hash=hash_password("123456"),
            full_name="System Admin",
            role="ADMIN",
            is_active=True
        )

        manager = User(
            email="manager@gmail.com",
            password_hash=hash_password("123456"),
            full_name="Project Manager",
            role="USER",
            is_active=True
        )

        employee = User(
            email="employee@gmail.com",
            password_hash=hash_password("123456"),
            full_name="Construction Employee",
            role="USER",
            is_active=True
        )

        db.add_all([
            admin,
            manager,
            employee
        ])

        db.flush()


        site = ConstructionSite(
            name="Công trình nhà ở Hà Nội",
            description="Công trình nhà ở 5 tầng",
            owner_id=manager.id
        )

        db.add(site)

        db.flush()


        owner_member = SiteMember(
            site_id=site.id,
            user_id=manager.id,
            role="OWNER"
        )

        employee_member = SiteMember(
            site_id=site.id,
            user_id=employee.id,
            role="MEMBER"
        )

        db.add_all([
            owner_member,
            employee_member
        ])


        work1 = WorkItem(
            site_id=site.id,
            title="Thi công móng",
            description="Thi công phần móng công trình",
            assignee_id=employee.id,
            status="DONE",
            priority="HIGH"
        )

        work2 = WorkItem(
            site_id=site.id,
            title="Xây tầng 1",
            description="Xây dựng tầng 1",
            assignee_id=employee.id,
            status="IN_PROGRESS",
            priority="HIGH"
        )

        work3 = WorkItem(
            site_id=site.id,
            title="Lắp đặt hệ thống điện",
            description="Lắp đặt hệ thống điện",
            assignee_id=None,
            status="TODO",
            priority="MEDIUM"
        )

        db.add_all([
            work1,
            work2,
            work3
        ])

        db.commit()

        print("================================")
        print("Seed data successfully!")
        print("================================")
        print("Admin:")
        print("Email: admin@gmail.com")
        print("Password: 123456")
        print()
        print("Manager:")
        print("Email: manager@gmail.com")
        print("Password: 123456")
        print()
        print("Employee:")
        print("Email: employee@gmail.com")
        print("Password: 123456")

    except Exception as e:
        db.rollback()
        print("Seed failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed()