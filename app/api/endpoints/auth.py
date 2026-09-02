from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Any
import uuid

from app.db.database import get_db
from app.db import models
from app.schemas import user as user_schema
from app.core import security
from app.core.config import settings
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: user_schema.UserCreate, db: Session = Depends(get_db)) -> Any:
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    if len(user_in.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long."
        )
    
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=user_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/guest", response_model=user_schema.Token)
def guest_login(db: Session = Depends(get_db)) -> Any:
    # See if Demo Account exists
    demo_account = db.query(models.CustomerAccount).filter(models.CustomerAccount.name == "Demo Account").first()
    if not demo_account:
        demo_account = models.CustomerAccount(name="Demo Account", plan="Standard")
        db.add(demo_account)
        db.commit()
        db.refresh(demo_account)
        
        # Add a demo shipment for the guest view
        admin_user = db.query(models.User).filter(models.User.role == models.Role.ADMIN).first()
        admin_id = admin_user.id if admin_user else 1
        
        demo_ship = models.Shipment(
            tracking_id="PP-DEMO-1001",
            account_id=demo_account.id,
            customer_id=admin_id,
            sender_name="Demo Company",
            receiver_name="Guest User",
            origin="Hyderabad",
            destination="Bangalore"
        )
        db.add(demo_ship)
        db.commit()

    guest_id = str(uuid.uuid4())[:8]
    email = f"guest_{guest_id}@guest.parcelpilot.com"
    
    db_user = models.User(
        name=f"Guest User {guest_id}",
        email=email,
        account_id=demo_account.id,
        hashed_password=security.get_password_hash(uuid.uuid4().hex),
        role=models.Role.GUEST
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token_expires = timedelta(minutes=60) # 1 hour session
    access_token = security.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=user_schema.UserResponse)
def read_users_me(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return current_user
