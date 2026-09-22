from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import User, Role, Driver
from app.schemas.driver import DriverCreate
from app.core.security import get_password_hash


def create_driver(db: Session, driver_in: DriverCreate, account_id: int | None = None) -> dict:
    if db.query(User).filter(User.email == driver_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(Driver).filter(Driver.vehicle_number == driver_in.vehicle_number).first():
        raise HTTPException(status_code=400, detail="Vehicle number already registered")

    if account_id is None:
        raise HTTPException(status_code=400, detail="Admin must belong to an account")

    user = User(
        name=driver_in.name,
        email=driver_in.email,
        hashed_password=get_password_hash(driver_in.password),
        role=Role.DRIVER,
        account_id=account_id,
    )
    db.add(user)
    db.flush()

    driver = Driver(
        user_id=user.id,
        phone=driver_in.phone,
        vehicle_number=driver_in.vehicle_number,
        vehicle_type=driver_in.vehicle_type,
    )
    db.add(driver)
    db.commit()
    db.refresh(driver)
    db.refresh(user)

    return {
        "id": driver.id,
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": driver.phone,
        "vehicle_number": driver.vehicle_number,
        "vehicle_type": driver.vehicle_type,
        "is_available": driver.is_available,
        "assigned_shipments_count": 0,
        "created_at": driver.created_at,
    }


def list_drivers(db: Session, account_id: int | None, skip: int = 0, limit: int = 100):
    if account_id is None:
        return []

    drivers = (
        db.query(Driver)
        .join(User, Driver.user_id == User.id)
        .filter(User.account_id == account_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    results = []
    for driver in drivers:
        results.append(
            {
                "id": driver.id,
                "user_id": driver.user_id,
                "name": driver.user.name,
                "email": driver.user.email,
                "phone": driver.phone,
                "vehicle_number": driver.vehicle_number,
                "vehicle_type": driver.vehicle_type,
                "is_available": driver.is_available,
                "assigned_shipments_count": len(driver.assigned_shipments),
                "created_at": driver.created_at,
            }
        )
    return results
